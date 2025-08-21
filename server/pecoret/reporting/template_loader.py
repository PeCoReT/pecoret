import importlib.util
import sys
from pathlib import Path
from django.conf import settings
from django.core.exceptions import ValidationError, ImproperlyConfigured


class ReportTemplateLoader:
    def __init__(self, dict_key):
        """
        dict_key: key name from `settings.REPORT_TEMPLATES`. aka template_name
        """
        self.template_meta = settings.REPORT_TEMPLATES.get(dict_key, {})
        self.template_name = dict_key
        if self.template_meta.get('path'):
            self.template_directory, self.filename = self._init_from_path(self.template_meta)
        elif self.template_meta.get('preset'):
            self.template_directory, self.filename = self._init_from_preset(self.template_meta)
        else:
            raise ImproperlyConfigured('report template requires a preset or path')
        if self.template_directory is None:
            raise ValidationError({'template': 'Template not configured in settings!'})

    def _init_from_preset(self, meta):
        preset = meta.get('preset')
        data = None
        if settings.REPORT_TEMPLATE_PRESETS.get(preset):
            data = settings.REPORT_TEMPLATE_PRESETS[preset]
        elif settings.REPORT_TEMPLATES.get(preset):
            data = settings.REPORT_TEMPLATES[preset]
        if not data:
            raise ImproperlyConfigured('invalid preset')
        return self._init_from_path(data)

    @staticmethod
    def _init_from_path(meta):
        directory = Path(meta.get('path')).parent
        filename = str(meta.get('path')).split("/")[-1]
        return directory, filename

    def import_module(self):
        try:
            template_file = f'{self.template_directory}/{self.filename}'
            spec = importlib.util.spec_from_file_location(self.template_name, template_file)
            if not spec:
                raise ImportError('no spec')
            module = importlib.util.module_from_spec(spec)
            if not module:
                raise ImportError('no module')
        except ImportError as e:
            print(e)
            raise ValidationError({'template': 'Could not import template module!'})
        if not spec:
            raise ValidationError({'template': 'Could not import template module!'})
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module

    def load(self):
        module = self.import_module()
        report_template = getattr(module, 'ReportTemplate')(self.template_directory, meta=self.template_meta)
        return report_template
