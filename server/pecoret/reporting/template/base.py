import datetime
from pathlib import Path

from pecoret.core.utils import image64
from pecoret.core.utils.markdown import bleach_md
from pecoret.reporting.template.mixins import ReportErrorMixin
from pecoret.reporting import generators


class BaseReportTemplate:
    css_files = []

    def __init__(self, main_directory, **kwargs):
        self.main_directory = main_directory
        self.templates_directory = Path(self.main_directory, "templates")
        self.kwargs = kwargs

    def get_context(self, **kwargs):
        kwargs.setdefault('template', self)
        kwargs.setdefault('report_helpers', {
            'bleach_md': bleach_md,
            'image64': image64
        })
        kwargs.setdefault('now', datetime.datetime.now().strftime('%B %d, %Y'))
        return kwargs

    def on_preprocess(self, generator, **kwargs):
        if isinstance(generator, generators.PDFReportGenerator):
            # set css files to hardcoded css_files for this template
            generator.css_files += self._get_css_files()

    def _get_css_files(self):
        css_files = self.css_files.copy()
        css_files += self.kwargs.get('meta', {}).get('css_files', [])
        return css_files

    def on_postprocess(self, generator, result):
        return result

    def export_project_pdf_report(self, report_document):
        """
        used to generate the PDF Report for a project
        """
        raise NotImplementedError

    def export_single_finding(self, finding):
        raise NotImplementedError

    def export_attack_surface_finding(self, finding):
        raise NotImplementedError

    def export_advisory_pdf(self, advisory):
        raise NotImplementedError


class GenericReportTemplate(ReportErrorMixin, BaseReportTemplate):
    pass
