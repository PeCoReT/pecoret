from django.core.exceptions import ImproperlyConfigured
from pecoret.reporting import mixins
from pecoret.core.utils.markdown import bleach_md
from pecoret.core.utils import image64


class BaseTemplate(mixins.ContextMixin, mixins.ErrorMixin):
    content_type = None
    file_extension = None

    def pre_processing(self, *args, **kwargs):
        self.check_report_errors()

    def post_processing(self, rendered_report, *args, **kwargs):
        pass

    def render_report(self):
        raise NotImplementedError()

    def generate(self, *args, **kwargs):
        self.pre_processing(*args, **kwargs)
        rendered_report = self.render_report()
        self.post_processing(rendered_report, *args, **kwargs)
        return rendered_report

    def get_context(self):
        context = super().get_context()
        context["report_helpers"] = {
            "bleach_md": bleach_md,
            "image64": image64
        }
        context["template"] = self
        return context


class BasePDFTemplate(mixins.PDFMixin, BaseTemplate):
    def render_report(self):
        return self.render_pdf(self.get_context())


class ProjectPDFTemplate(BasePDFTemplate):
    def __init__(self, report_template, *args, **kwargs):
        super().__init__(report_template, *args, **kwargs)
        self.report_document = kwargs.get('report_document')
        if not self.report_document:
            raise ImproperlyConfigured("report_document must be set")
        self._activate_translation_lang(self.get_project().language)

    def get_project(self):
        return self.report_document.report.project

    def post_processing(self, rendered_report, *args, **kwargs):
        self.report_document.compiled_source = rendered_report
        self.report_document.content_type = self.content_type
        self.report_document.file_extension = self.file_extension
        self.report_document.save()


class SingleFindingPDFTemplate(BasePDFTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.finding = kwargs.get('finding')
        if not self.finding:
            raise ImproperlyConfigured('SingleFindingPDFTemplate must have finding')
        self._activate_translation_lang(self.get_project().language)

    def get_project(self):
        return self.finding.project


class BaseExcelTemplate(mixins.ExcelMixin, BaseTemplate):
    file_extension = "xlsx"
    content_type = "application/vnd.ms-excel"

    def render_report(self):
        return self.render_excel(self.get_context())


class ProjectExcelTemplate(BaseExcelTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report_document = kwargs.get('report_document')
        if not self.report_document:
            raise ImproperlyConfigured("report_document must be set")

    def get_project(self):
        return self.report_document.report.project

    def post_processing(self, rendered_report, *args, **kwargs):
        self.report_document.compiled_source = rendered_report
        self.report_document.content_type = self.content_type
        self.report_document.file_extension = self.file_extension
        self.report_document.save()


class AdvisoryMarkdownTemplate(mixins.JinjaMixin, BaseTemplate):
    content_type = "text/plain"
    file_extension = "md"
    template_file = "advisory.md"

    def __init__(self, *args, **kwargs):
        if "advisory" not in kwargs:
            raise ImproperlyConfigured
        super().__init__(*args, **kwargs)
        self.advisory = kwargs["advisory"]

    def get_context(self):
        context = super().get_context()
        context["advisory"] = self.advisory
        return context

    def render_report(self):
        return self.render_to_string(self.get_context())


class AdvisoryPDFTemplate(BasePDFTemplate):

    def __init__(self, *args, **kwargs):
        if "advisory" not in kwargs:
            raise ImproperlyConfigured
        super().__init__(*args, **kwargs)
        self.advisory = kwargs['advisory']

    def get_context(self):
        context = super().get_context()
        context['advisory'] = self.advisory
        return context


class VulnerabilityCSVTemplate(mixins.ProjectRelatedMixin, mixins.JinjaMixin, BaseTemplate):
    content_type = "plain/text"
    file_extension = "csv"
    default_Title = "Vulnerability CSV"
    template_file = "vulnerability_overview.csv"

    def render_report(self):
        return self.render_to_string(self.get_context()).encode()
