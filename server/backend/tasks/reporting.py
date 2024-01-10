from pecoret.reporting.report_plugin import ReportPluginLoader
from backend.models.reports.report_release import ReportRelease
from backend.models.reports.report import ReportVariant


def create_report_document_task(report_document_pk):
    report_document = ReportRelease.objects.get(pk=report_document_pk)
    # get the report variant (e.g. Pentest PDF)
    report_variant = ReportVariant(report_document.report.variant)
    plugin_loader = ReportPluginLoader(report_document.report.template)
    plugin = plugin_loader.load_plugin_from_report_template(report_variant.to_plugin_method)
    result, content_type, extension = getattr(plugin, report_variant.to_plugin_method)(report_document)
    report_document.compiled_source = result
    report_document.content_type = content_type
    report_document.file_extension = extension
    report_document.save()
    return result


def export_single_finding(finding, template):
    plugin_loader = ReportPluginLoader(template)
    plugin = plugin_loader.load_plugin_from_report_template('export_single_finding')
    result, content_type, extension = plugin.export_single_finding(finding)
    return result


def export_advisory(advisory, template):
    plugin_loader = ReportPluginLoader(template)
    plugin = plugin_loader.load_plugin_from_report_template('export_advisory_pdf')
    result, content_type, extension = plugin.export_advisory_pdf(advisory)
    return result
