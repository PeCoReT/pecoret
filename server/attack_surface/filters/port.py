from django_filters import rest_framework as filters
from pecoret.core.utils.filters import ChoiceFilter
from attack_surface.models.port import Port, Protocol
from .base import ProgramFilterMixin


class PortFilter(ProgramFilterMixin, filters.FilterSet):
    protocol = ChoiceFilter(choices=Protocol.choices)
    target = filters.NumberFilter(method='filter_target')
    is_web = filters.BooleanFilter(method='filter_is_web')

    def filter_target(self, queryset, name, value):
        return queryset.for_target(value)

    def filter_is_web(self, queryset, name, value):
        return queryset.is_web(value)

    class Meta:
        model = Port
        fields = [
            'number', 'protocol', 'service', 'host'
        ]
