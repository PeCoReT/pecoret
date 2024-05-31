from django_filters import rest_framework as filters
from pecoret.core.utils.filters import ChoiceFilter
from attack_surface.models.port import Port, Protocol
from attack_surface.models.target import Target
from .base import ProgramFilterMixin


class PortFilter(ProgramFilterMixin, filters.FilterSet):
    protocol = ChoiceFilter(choices=Protocol.choices)
    target = filters.ModelChoiceFilter(field_name='target', queryset=Target.objects.all())

    class Meta:
        model = Port
        fields = [
            'port', 'protocol', 'service', 'target'
        ]
