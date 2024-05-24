from pecoret.reporting.report_plugin import ReportPluginLoader
from asmonitor.utils.technology import get_nested_technologies
from asmonitor.models import URL


def export_finding(finding, template):
    plugin_loader = ReportPluginLoader(template)
    plugin = plugin_loader.load_plugin_from_report_template('export_asmonitor_finding')
    result, content_type, extension = plugin.export_asmonitor_finding(finding)
    return result


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
