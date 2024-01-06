from django.utils import translation
from django.core.exceptions import ImproperlyConfigured
from jinja2 import FileSystemLoader
from jinja2.sandbox import SandboxedEnvironment
from backend.models.reports.change_history import ChangeHistory
from pecoret.core.utils.markdown import bleach_md
from pecoret.core.utils import image64
from pecoret.core.reporting.jinja.utils import dynamic_trans


class BaseReportType:
    """the base report type that other report types must inherit from"""

    jinja_autoescape = True
    template_name = None
    content_type = None
    file_extension = None

    def __init__(self, report_template, *args, **kwargs):
        self.report_template = report_template
        self.jinja_loader = FileSystemLoader(self.report_template.template_path)
        self.jinja_env = SandboxedEnvironment(
            loader=self.jinja_loader,
            autoescape=self.jinja_autoescape,
            extensions=["jinja2.ext.i18n"],
        )
        self.enable_i18n()
        self.errors = {}

    def enable_i18n(self):
        # pylint: disable=no-member
        #self.jinja_env.install_gettext_callables(
        #    gettext=translation.gettext, ngettext=translation.ngettext, newstyle=True
        #)
        self.jinja_env.install_gettext_translations(translation)
        self.jinja_env.policies['ext.i18n.trimmed'] = True
        self.jinja_env.filters['dynamic_trans'] = dynamic_trans

    def _activate_translation_lang(self, lang):
        translation.activate(lang)

    def get_content_type(self):
        """get the content type for this type of report.
        Required to provide downloads.

        Raises:
            ImproperlyConfigured: _description_

        Returns:
            _type_: _description_
        """
        if not self.content_type:
            raise ImproperlyConfigured("No content type!")
        return self.content_type

    def get_file_extension(self):
        """get the file extension for this report type.
        e.g. '.pdf'

        Raises:
            ImproperlyConfigured: no file extension set.

        Returns:
            str: _description_
        """
        if not self.file_extension:
            raise ImproperlyConfigured("No file extension!")
        return self.file_extension

    def get_context(self):
        """the context that is passed to the jinja2 render function

        Returns:
            dict: the context that is passed to jinja2
        """
        return {
            "report_helpers": {
                "bleach_md": bleach_md,
                "image64": image64
            },
            "variant": self
        }

    def get_template_name(self):
        """just get the template name

        Raises:
            ImproperlyConfigured: no template_name set.

        Returns:
            str: the template name (e.g. report.html oder advisory.md)
        """
        if not self.template_name:
            raise ImproperlyConfigured
        return self.template_name

    def render_report(self):
        """must be implemented by all child classes.
        must return the result of the renderer process

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError

    def pre_processing(self, *args, **kwargs):
        self.check_report_errors()

    def post_processing(self, *args, **kwargs):
        pass

    def generate(self):
        """generated the report by doing pre processing, rendering and post processing steps.

        Returns:
            tuple: True and string if report was created
        """
        self.pre_processing()
        rendered_report = self.render_report()
        self.post_processing(rendered_report=rendered_report)
        return rendered_report

    def _add_error(self, error):
        if not self.errors.get(error.url):
            self.errors[error.url] = [error]
        else:
            self.errors[error.url].append(error)

    def check_report_errors(self):
        pass

    def get_errors(self):
        return self.errors

    def get_errors_for_section(self, section):
        return self.errors.get(section, [])



class ProjectRelatedReportType(BaseReportType):
    """report type specific to project related reports.
    this type adds project related information to the renderer context.
    """

    default_title = "Report"

    def __init__(self, report_template, report_document, *args, **kwargs):
        super().__init__(report_template, *args, **kwargs)
        self.report_document = report_document
        self._activate_translation_lang(self.get_project().language)

    def get_project(self):
        return self.report_document.report.project

    @property
    def version(self):
        qs = ChangeHistory.objects.filter(report=self.report_document.report)
        if qs.exists():
            return qs.order_by("-version").first()
        return "0.1"

    @property
    def title(self):
        custom_title = self.report_document.report.title
        if not custom_title:
            return self.default_title
        return custom_title

    def get_context(self):
        context = super().get_context()
        context["project"] = self.get_project()
        context["report_document"] = self.report_document
        return context

    def post_processing(self, *args, **kwargs):
        # self.report_document.raw_source = kwargs["raw_source"]
        self.report_document.compiled_source = kwargs["rendered_report"]
        self.report_document.content_type = self.get_content_type()
        self.report_document.file_extension = self.get_file_extension()
        self.report_document.save()
