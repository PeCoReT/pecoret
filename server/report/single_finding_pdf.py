from pecoret.reporting.template import SingleFindingPDFTemplate
from .base import DefaultBaseTemplate


class SingleFindingPDFReport(DefaultBaseTemplate, SingleFindingPDFTemplate):
    template_file = "single_finding_export.html"

    def check_report_errors(self):
        self.check_finding_errors()

    def get_context(self):
        context = super().get_context()
        context["finding"] = self.finding
        return context
