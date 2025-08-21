from pecoret.reporting.template_loader import ReportTemplateLoader
from backend.models.reports.report_release import ReportRelease


def create_report_document_task(report_document_pk):
    report_document = ReportRelease.objects.get(pk=report_document_pk)
    template_name = report_document.report.template
    loader = ReportTemplateLoader(template_name)
    report_template = loader.load()

    result, content_type, extension = report_template.export_project_pdf_report(report_document)

    report_document.compiled_source = result
    report_document.content_type = content_type
    report_document.file_extension = extension
    report_document.save()
    return result


def export_single_finding(finding, template):
    loader = ReportTemplateLoader(template)
    report_template = loader.load()
    result, _, _ = report_template.export_single_finding(finding)
    return result


def export_advisory(advisory, template):
    loader = ReportTemplateLoader(template)
    report_template = loader.load()
    result, _, _ = report_template.export_advisory_pdf(advisory)
    return result
