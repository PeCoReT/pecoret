import sys
from pathlib import Path
from django.utils import translation
from django.core.exceptions import ImproperlyConfigured
from jinja2 import FileSystemLoader
from jinja2.sandbox import SandboxedEnvironment
from pecoret.core.reporting.jinja.utils import dynamic_trans


class JinjaMixin:
    jinja_auto_escape = True
    template_file = None

    def __init__(self, *args, **kwargs):
        self.jinja_loader = FileSystemLoader(self.template_path)
        self.jinja_env = SandboxedEnvironment(
            loader=self.jinja_loader,
            autoescape=self.jinja_auto_escape,
            extensions=["jinja2.ext.i18n"],
        )
        self.enable_i18n()

    @property
    def template_dir(self):
        return Path(sys.modules[self.__module__].__file__).parent

    @property
    def template_path(self):
        path = self.template_dir / 'templates'
        return str(path)

    def get_template_file(self):
        if not self.template_file:
            raise ImproperlyConfigured("Template must have a template_file set.")
        return self.template_file

    def enable_i18n(self):
        self.jinja_env.install_gettext_translations(translation)
        self.jinja_env.policies['ext.i18n.trimmed'] = True
        self.jinja_env.filters['dynamic_trans'] = dynamic_trans

    def _activate_translation_lang(self, lang):
        translation.activate(lang)

    def render_to_string(self, context):
        template = self.jinja_env.get_template(self.get_template_file())
        return template.render(context)
