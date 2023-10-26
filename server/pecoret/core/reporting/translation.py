import os
import importlib
from pathlib import Path
from django.utils.translation.trans_real import DjangoTranslation
from django.conf import settings
from backend.models.report_templates import ReportTemplate


def patch_django_translation():
    """patch django translation to not use LOCALE_DIRS setting.
    Instead, we use the path stored in the ``ReportTemplate``.

    Source: https://stackoverflow.com/a/60221067
    """
    def _add_local_translations(self):
        packages = ReportTemplate.objects.active().values_list("package", flat=True)
        for package in packages:
            try:
                module = importlib.import_module(package)
            except ImportError:
                print(f"Could not import {package}")
                continue
            template_directory = Path(module.__file__).parent
            locale_dir = template_directory / 'locale'
            translation = self._new_gnu_trans(locale_dir)
            self.merge(translation)
        self.merge(self._new_gnu_trans(str(settings.BASE_DIR / "locale")))

    DjangoTranslation._add_local_translations = _add_local_translations
