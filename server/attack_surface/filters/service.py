from django_filters import rest_framework as filters
from attack_surface.models.service import Service
from .base import ProgramFilterMixin


class ServiceFilter(ProgramFilterMixin, filters.FilterSet):
    is_web = filters.BooleanFilter(method='filter_is_web')

    def filter_is_web(self, queryset, name, value):
        return queryset.is_web(value)

    class Meta:
        model = Service
        fields = [
            'is_web'
        ]
