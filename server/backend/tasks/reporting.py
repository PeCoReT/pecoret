from backend.models.reports.report_release import ReportRelease
from backend.models.reports.report import ReportVariant
from pecoret.reporting.template import TemplateLoader


def create_report_document_task(report_document_pk):
    report_document = ReportRelease.objects.get(pk=report_document_pk)
    # get the report variant (e.g. Pentest PDF)
    report_variant = ReportVariant(report_document.report.variant)
    loader = TemplateLoader(report_document.report.template)
    # pylint: disable=invalid-name
    RenderableReport = loader.load_template_for_variant(report_variant)
    result = RenderableReport(loader.template, report_document=report_document).generate()
    return result
