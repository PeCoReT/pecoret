from django_filters import rest_framework as filters
from attack_surface.models.url import URL
from attack_surface.models.service import Service
from .base import TagTechnologyFilter, ProgramFilterMixin


class URLFilter(ProgramFilterMixin, TagTechnologyFilter):
    service = filters.ModelChoiceFilter(field_name='service', queryset=Service.objects.all())

    class Meta:
        model = URL
        fields = [
            'is_base', 'tags', 'technologies', 'url', 'status_code', 'service'
        ]
