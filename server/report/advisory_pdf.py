import datetime
from pecoret.reporting.template import AdvisoryPDFTemplate
from .base import DefaultBaseTemplate


class AdvisoryPDFExport(AdvisoryPDFTemplate, DefaultBaseTemplate):
    template_file = "advisory_export.html"

    def get_context(self):
        context = super().get_context()
        context["now"] = datetime.datetime.now().strftime("%B %d, %Y")
        return context
