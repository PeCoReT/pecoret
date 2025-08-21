from datetime import timedelta
from itertools import islice

from django.db.models import Max
from django.utils import timezone

from attack_surface.scanning.models import ExclusionRule
from attack_surface.scanning.models.scan_batch import ScanBatchRequest, StatusChoices, TriggerSource
from attack_surface.scanning.models.scan_template import ScanTemplate, InputTypeChoices


def scheduler_task(name=None):
    check_pending_trickles()

    templates = ScanTemplate.objects.enabled()
    if name:
        templates = templates.filter(name__icontains=name)

    for template in templates:
        process_template_batches(template)


def process_template_batches(template):
    now = timezone.now()
    rate_limit_window_start = now - timedelta(days=1)

    if template.rate_limit is not None:
        recent_batches_count = ScanBatchRequest.objects.filter(
            scan_template=template,
            date_created__gte=rate_limit_window_start
        ).count()
        batches_remaining = template.rate_limit - recent_batches_count
        if batches_remaining <= 0:
            return
    else:
        batches_remaining = float("inf")

    qs = get_eligible_items(template)
    qs = apply_cooldown(qs, template)

    item_iterator = qs.iterator()
    batch = None
    batch_size = template.batch_threshold

    while True:
        chunk = list(islice(item_iterator, batch_size))
        if not chunk or batches_remaining <= 0:
            break

        batch = ScanBatchRequest.objects.create(
            scan_template=template,
            scan_trigger_source=TriggerSource.CONTINUOUS,
            status=StatusChoices.STAGING
        )
        batch.add_items(chunk)
        if batch.get_item_field().count() >= batch_size:
            batch.mark_full()
        batches_remaining -= 1


def check_pending_trickles():
    now = timezone.now()
    for batch in ScanBatchRequest.objects.with_status(StatusChoices.STAGING):
        template = batch.scan_template
        if not template.trickle_delay or not batch.date_last_item_added:
            continue
        timeout_seconds = template.trickle_delay.total_seconds()
        elapsed = (now - batch.date_last_item_added).total_seconds()
        if elapsed >= timeout_seconds:
            batch.mark_full()


def get_eligible_items(template):
    Model = template.InputTypes.get_related_item_class(template.input_type)
    if not Model:
        raise Exception("unknown input type. should not happen!")

    qs = Model.objects.all()
    if template.input_type != InputTypeChoices.PROGRAMS:
        qs = Model.objects.in_scope()
        if template.conditions:
            qs = qs.djangoql(template.conditions)

    qs = qs.exclude(
        scan_batches__scan_template=template,
        scan_batches__status__in=[
            StatusChoices.PENDING,
            StatusChoices.IN_PROGRESS,
            StatusChoices.STAGING
        ]
    )
    return apply_exclusions(template, qs)


def apply_cooldown(items, template):
    cooldown = template.cooldown
    if not cooldown:
        return items

    now = timezone.now()
    recent_scan_pks = ScanBatchRequest.objects.with_template(template).annotate(
        last_time=Max('batch_end_time')
    ).filter(batch_end_time__isnull=False).filter(
        batch_end_time__gt=now - cooldown
    ).values_list(f"{template.input_type}__id", flat=True)

    return items.exclude(pk__in=recent_scan_pks)


def apply_exclusions(template, items):
    rules = ExclusionRule.objects.with_scan_template(template)
    programs = rules.distinct_item_pks("program")

    if programs and template.input_type != InputTypeChoices.PROGRAMS:
        items = items.exclude_programs(programs)
    if programs and template.input_type == InputTypeChoices.PROGRAMS:
        items = items.exclude(pk__in=programs)
    if template.input_type == InputTypeChoices.TARGETS:
        items = items.exclude(pk__in=rules.distinct_item_pks("target"))
    elif template.input_type == InputTypeChoices.SERVICES:
        targets = rules.distinct_item_pks("target")
        if targets:
            items = items.exclude(target__in=targets)
        items = items.exclude(pk__in=rules.distinct_item_pks("service"))
    elif template.input_type == InputTypeChoices.URLS:
        items = items.exclude(pk__in=rules.distinct_item_pks("url"))

    return items

