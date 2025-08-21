from django.conf import settings
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        kwargs['settings'] = {
            'PECO_THEME': f'{settings.PECO_THEME}.css',
        }
        return super().get_context_data(**kwargs)
