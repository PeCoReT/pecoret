from attack_surface.models.url import URL
from .base import TagTechnologyFilter, ProgramFilterMixin


class URLFilter(ProgramFilterMixin, TagTechnologyFilter):
    class Meta:
        model = URL
        fields = [
            'is_base', 'tags', 'technologies', 'url', 'program', 'status_code'
        ]
