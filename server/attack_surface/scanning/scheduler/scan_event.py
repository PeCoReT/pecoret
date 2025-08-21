from urllib.parse import urlparse

from django.utils import timezone
from django_q.tasks import async_task

from attack_surface.models.tag import Tag
from backend.models import Technology
from attack_surface.models import Target, URL, ScopeItem, Program
from attack_surface.models.service import Protocol, Service
from attack_surface.scanning.models import ScanRule, ScanBatchRequest
from attack_surface.scanning.models.scan_batch import StatusChoices
from attack_surface.utils import get_domain_from_subdomain


def scanner_event_parser_task(batch_id, event_type, payload):
    # event received by scanner. this is the entrypoint for parsing
    if event_type in [
        "discovery.url",
        "discovery.url-bulk",
        "discovery.target",
        "discovery.target-bulk",
        "discovery.service",
        "discovery.service-bulk",
    ]:
        # try to offload heavy queries into async tasks
        async_task(on_default_event, batch_id, event_type, payload)
        # on_default_event(batch_id, event_type, payload)
        return
    # batch events
    if event_type == "batch.started":
        batch = ScanBatchRequest.objects.get(pk=batch_id)
        batch.batch_start_time = timezone.now()
        batch.save()
        return
    if event_type == "batch.finished":
        batch = ScanBatchRequest.objects.get(pk=batch_id)
        batch.status = StatusChoices.COMPLETED
        batch.batch_end_time = timezone.now()
        batch.raw_output = payload.get("output")
        batch.errors = payload.get("errors")
        batch.save()
        return
    if event_type == "batch.error":
        batch = ScanBatchRequest.objects.get(pk=batch_id)
        batch.batch_end_time = timezone.now()
        batch.status = StatusChoices.FAILED
        batch.errors = payload.get("errors")
        batch.save()
        return
    # check if we have a rule for this one
    rules = ScanRule.objects.with_event_type(event_type)
    if not rules.exists():
        # not a rule that is configured yet, returning
        return
    # TODO: implement logic here to handle custom events
    return rules


def on_default_event(batch_id, event_type, payload):
    # _ = ScanBatchRequest.objects.get(pk=batch_id)
    if event_type == "discovery.url":
        on_discovery_url(payload["payload"])
    elif event_type == "discovery.target":
        on_discovery_target(payload["payload"])
    elif event_type == "discovery.service":
        on_discovery_service(payload["payload"])
    elif event_type == "discovery.service-bulk":
        for p in payload["bulk"]:
            on_discovery_service(p)
    elif event_type == "discovery.url-bulk":
        for p in payload["bulk"]:
            on_discovery_url(p)
    elif event_type == "discovery.target-bulk":
        for p in payload["bulk"]:
            on_discovery_target(p)


def on_discovery_target(payload):
    if payload.get("pk"):
        pk = payload.pop("pk")
        target = Target.objects.get(pk=pk)
        for field, value in payload.items():
            setattr(target, field, value)
        target.save()
        return
    program = payload.pop("program", None)
    if not program:
        program = fuzzy_guess_target_program(payload["data"])
    else:
        program = Program.objects.get(pk=program)
    Target.objects.update_or_create(
        data=payload["data"], program=program, defaults=payload
    )


def on_discovery_service(payload):
    target_data = payload.pop("target", None)
    technologyData = payload.pop("technologies", [])
    tagData = payload.pop("tags", [])

    if tagData is None:
        tagData = []
    if technologyData is None:
        technologyData = []
    if payload.get("protocol"):
        payload["protocol"] = Protocol[payload["protocol"]].value
    if target_data and target_data.get("pk"):
        target = Target.objects.get(pk=target_data["pk"])
        for field, value in target_data.items():
            setattr(target, field, value)
        target.save()
    elif target_data and target_data.get("data"):
        target = Target.objects.get_or_create(
            data=target_data["data"], defaults=target_data
        )[0]
    else:
        # INVALID PAYLOAD?
        print("INVALID PAYLOAD for service!")
        return
    service, created = Service.objects.update_or_create(
        target=target,
        port_number=payload["port_number"],
        protocol=payload["protocol"],
        defaults=payload,
    )
    if created and not service.service_name:
        service.service_name = "unknown"
    techs = handle_technologies(technologyData)
    service.technologies.add(*techs)

    tags = handle_tags(tagData)
    service.tags.add(*tags)
    service.save()


def handle_technologies(cpes):
    pks = set()
    for cpe in cpes:
        tech, _ = Technology.objects.get_or_create(cpe=cpe, defaults={"name": cpe})
        pks.add(tech.pk)
    return Technology.objects.filter(pk__in=pks).only("pk")


def handle_tags(names):
    pks = set()
    for name in names:
        tag, _ = Tag.objects.get_or_create(name=name)
        pks.add(tag.pk)
    return Tag.objects.filter(pk__in=pks).only("pk")


def on_discovery_url(payload):
    service_payload = payload.pop("service", {})
    techData = payload.pop("technologies", [])
    tagData = payload.pop("tags", [])
    if techData is None:
        techData = []
    if tagData is None:
        tagData = []

    if payload.get("pk"):
        pk = payload.pop("pk")
        url = URL.objects.get(pk=pk)
        for field, value in payload.items():
            setattr(url, field, value)

        # set tags and techs
        techs = handle_technologies(techData)
        url.technologies.add(*techs)

        tags = handle_tags(tagData)
        url.tags.add(*tags)
        url.save()
        return
    if not service_payload.get("pk"):
        # try to find it ourselves
        parsed = urlparse(payload["url"])
        program = fuzzy_guess_target_program(parsed.hostname)
        if program is None:
            program = Program.objects.get_or_create(name="Scanner Discoveries")[0]
        target = Target.objects.get_or_create(data=parsed.hostname, program=program)[0]
        service_payload["service_name"] = parsed.scheme
        data = {
            "target": target,
            "protocol": Protocol.TCP,
            "banner": payload.get("response"),
        }
        if parsed.port:
            data["port_number"] = parsed.port
        else:
            if parsed.scheme == "http":
                data["port_number"] = 80
            else:
                data["port_number"] = 443
        service = Service.objects.get_or_create(**data, defaults=service_payload)[0]
        # only update this one because previous steps were just needed to "guess" correct instance
        url = URL.objects.update_or_create(
            url=payload["url"], service=service, defaults=payload
        )[0]
        techs = handle_technologies(techData)
        url.technologies.add(*techs)
        tags = handle_tags(tagData)
        url.tags.add(*tags)
        url.save()


def fuzzy_guess_target_program(data):
    if Target.objects.filter(data=data).values("pk").exists():
        return Target.objects.get(data=data).program
    domain = get_domain_from_subdomain(data)
    # search for scope data
    scope_items = ScopeItem.objects.domains().filter(value=domain)
    if scope_items.exists():
        if scope_items.includes().exists():
            item = scope_items.includes().first()
            return item.scope.program
        elif scope_items.exclude().exists():
            item = scope_items.exclude().first()
            return item.scope.program
    return None
