from django.utils import translation
from django.core.exceptions import ImproperlyConfigured
from jinja2.sandbox import SandboxedEnvironment
from jinja2 import PackageLoader
from pecoret.reporting.utils import dynamic_trans
from pecoret.core.utils import image64
from pecoret.core.utils.markdown import bleach_md


class BaseReportGenerator:
    """
    base report generator. should be used as a base for other generators (e.g. PDFReportGenerator)
    """
    content_type = None
    file_extension = None
    jinja_autoescape = True

    def __init__(self, report_plugin, context, language=None, preprocess_cb=None, postprocess_cb=None):
        self.context = context
        self.report_plugin = report_plugin
        self.preprocess_cb = preprocess_cb
        self.postprocess_cb = postprocess_cb
        self.jinja_loader = PackageLoader(self.report_plugin.template_package, 'templates')
        self.jinja_env = SandboxedEnvironment(
            loader=self.jinja_loader,
            autoescape=self.jinja_autoescape,
            extensions=["jinja2.ext.i18n"],
        )
        if language:
            self.activate_translation_lang(language)

    @property
    def report_template(self):
        return self.report_plugin.report_template

    def _preprocess(self):
        """
        pre-process the report before it is rendered
        :return: None
        """
        self._enable_i18n()
        if self.preprocess_cb:
            self.preprocess_cb()

    def _postprocess(self, result):
        """
        post-processes the report after it was generated

        :return: None
        """
        if self.postprocess_cb:
            self.postprocess_cb(result)

    def generate(self, entry):
        """

        :param entry: template file to start with (e.g. pentest_report.html)
        :return:
        """
        raise NotImplementedError()

    def _enable_i18n(self):
        self.jinja_env.install_gettext_translations(translation)
        self.jinja_env.policies['ext.i18n.trimmed'] = True
        self.jinja_env.filters['dynamic_trans'] = dynamic_trans

    def activate_translation_lang(self, language):
        translation.activate(language)

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


class ReportGenerator(BaseReportGenerator):
    pass
