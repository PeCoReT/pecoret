import time
from django.apps import apps
from django.conf import settings
from attack_surface.models import URL, ScanType
from attack_surface.queue import enqueue_scan
from attack_surface.serializers.scanning.scan import ScanSerializer
from attack_surface.utils.technology import get_nested_technologies
from pecoret.reporting.template_loader import ReportTemplateLoader


def sync_implicit_techs_url(url_pk):
    """
    sync implicit technologies to the URL instance
    """
    try:
        url = URL.objects.get(pk=url_pk)
    except URL.DoesNotExist:
        # url seems to be removed in the meantime
        return

    technologies = get_nested_technologies(url)
    for tech in technologies:
        url.technologies.add(tech)
    url.save()


def enqueue_for_scan_seed(app_label, pk):
    app_name, model_name = app_label.split(".")
    model = apps.get_model(app_name, model_name.lower())

    try:
        obj = model.objects.get(pk=pk)
    except model.DoesNotExist:
        return
    scan_types = ScanType.objects.for_asset(obj).enabled().filter(name__in=settings.AS_ALLOWED_SCAN_TYPES_ON_CREATION)
    previous_job = None
    job = None
    for scan_type in scan_types.order_by('-priority'):
        # create a new scan with this scan type
        scan_name = f'Initial {scan_type.name} for {model_name}:{pk}:{str(int(time.time()))}'
        scan_data = {
            'name': scan_name,
            'scan_objects': [{'content_type': model_name.lower(), 'object_id': pk}], 'scan_type': scan_type.pk}
        serializer = ScanSerializer(data=scan_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if job:
            previous_job = job
        job = enqueue_scan(serializer.data, depends_on=previous_job)


def export_finding_pdf(finding, template):
    loader = ReportTemplateLoader(template)
    report_template = loader.load()
    result, _, _ = report_template.export_attack_surface_finding_pdf(finding)
    return result
