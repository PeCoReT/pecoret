import os
from django.utils.translation.trans_real import DjangoTranslation
from django.conf import settings


def patch_django_translation():
    """patch django translation to not use LOCALE_DIRS setting.
    Instead, we use the path stored in the ``ReportTemplate``.

    Source: https://stackoverflow.com/a/60221067
    """
    def _add_local_translations(self):
        template_names = list(settings.REPORT_TEMPLATES.keys())
        for name in reversed(template_names):
            path = settings.REPORT_TEMPLATES[name].get('path')
            if not path:
                continue
            locale_dir = os.path.join(path, "locale")
            translation = self._new_gnu_trans(locale_dir)
            self.merge(translation)
        self.merge(self._new_gnu_trans(str(settings.BASE_DIR / "locale")))

    DjangoTranslation._add_local_translations = _add_local_translations
