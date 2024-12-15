from django.conf import settings
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        kwargs['settings'] = {
            'PECO_THEME_INIT_BG_COLOR': settings.PECO_THEME_INIT_BG_COLOR,
            'PECO_THEME': settings.PECO_THEME,
        }
        return super().get_context_data(**kwargs)
