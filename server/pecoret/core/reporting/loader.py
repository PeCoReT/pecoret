import importlib.util
from pathlib import Path
from backend.models import ReportTemplate
from django.conf import settings


class RenderableLoader:
    """load the different renderable report variants from templates
    """
    def __init__(self, report_template, *args, **kwargs):
        self.report_template = report_template

    def load_fallback_template(self, class_name):
        """load the configured `FALLBACK_REPORT_TEMPLATE`.

        Args:
            class_name (str): the name of the report variant python class (e.g. PentestPDFReport)

        Returns:
            _type_: imported template module
        """
        self.report_template = ReportTemplate.objects.get(
            name=settings.FALLBACK_REPORT_TEMPLATE
        )
        template_module = self._import_template_module()
        template_class = getattr(template_module, class_name)
        return template_class

    def _import_template_module(self):
        module = importlib.import_module('extensions.report_templates.' + self.report_template.name + '.report')
        return module

    def load_template_class(self, class_name):
        """imports the custom report template from file path

        Args:
            class_name (str): The class name of the used report variant. (e.g. PDFReport)

        Returns:
            cls: the report variant class
        """
        try:
            template_module = self._import_template_module()
            template_class = getattr(template_module, class_name)
            return template_class
        # pylint: disable=broad-exception-caught
        except Exception as error:
            print(error)
            return self.load_fallback_template(class_name)

    def load_template_class_for_variant(self, variant):
        """load the template renderable class for a given variant

        Args:
            variant (ReportVariant): The variant we are looking for (e.g. VulnerabilityCSV)

        Returns:
            cls: the report variant class
        """
        return self.load_template_class(variant.variant_report_class_name)
