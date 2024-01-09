import datetime
import importlib
from pathlib import Path
from django.conf import settings

from pecoret.core.utils import image64
from pecoret.core.utils.markdown import bleach_md


class BaseReportPlugin:
    def __init__(self, report_template):
        self.report_template = report_template

    def get_context(self, **kwargs):
        kwargs.setdefault('report_plugin', self)
        kwargs.setdefault('report_helpers', {
            'bleach_md': bleach_md,
            'image64': image64
        })
        kwargs.setdefault('now', datetime.datetime.now().strftime('%B %d, %Y'))
        return kwargs

    @property
    def template_package(self):
        return f'extensions.report_templates.{self.report_template.name}'

    @property
    def template_directory(self):
        return Path(settings.EXTENSIONS_DIRECTORY / f'report_templates/{self.report_template.name}/templates')


class ReportPluginLoader:
    core_module = 'extensions.report_templates.{name}.plugin'

    def __init__(self, report_template):
        self.report_template = report_template

    def _load_fallback_template_module(self):
        module = importlib.import_module(self.core_module.format(name=settings.FALLBACK_REPORT_TEMPLATE))
        return module

    def load_plugin_from_report_template(self, render_method):
        """
        load a plugin from the ``ReportTemplate`` class.
        if report plugin module does not exist, import the fallback default template

        :return: module of the plugin's ``ReportPlugin``
        """
        try:
            module = importlib.import_module(self.core_module.format(name=self.report_template.name))
        except ImportError:
            module = self._load_fallback_template_module()
        plugin = getattr(module, 'ReportPlugin')(self.report_template)
        if not hasattr(plugin, render_method):
            # plugin does not implement required method, switch to default template
            plugin = getattr(self._load_fallback_template_module(), 'ReportPlugin')(self.report_template)
        return plugin
