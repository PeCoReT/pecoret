from django.utils.module_loading import import_string
from django.conf import settings
from backend.models import ReportTemplate


class TemplateLoader:
    def __init__(self, template):
        self.template = template

    def load_template_class(self, class_name, **kwargs):
        try:
            template_class = import_string(f"{self.template.package}.{class_name}")
        except ImportError as error:
            print(error)
            fallback = ReportTemplate.objects.get(name=settings.FALLBACK_REPORT_TEMPLATE)
            template_class = import_string(f"{fallback.package}.{class_name}")
        return template_class

    def load_template_for_variant(self, variant):
        return self.load_template_class(variant.variant_report_class_name)
