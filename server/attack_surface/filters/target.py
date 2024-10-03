from django_filters import BooleanFilter
from pecoret.core.utils.filters import ChoiceFilter
from attack_surface.models.target import Target, ScopeChoices, DataTypes
from .base import TagTechnologyFilter, ProgramFilterMixin


class TargetFilter(ProgramFilterMixin, TagTechnologyFilter):
    scope = ChoiceFilter(choices=ScopeChoices.choices)
    data_type = ChoiceFilter(choices=DataTypes.choices)
    is_resolved = BooleanFilter(method='filter_is_resolved')

    def filter_is_resolved(self, queryset, _name, value):
        if value is True:
            qs = queryset.filter(resolved_ip__isnull=False)
        else:
            qs = queryset.exclude(resolved_ip__isnull=False)
        return qs

    class Meta:
        model = Target
        fields = [
            'tags', 'technologies', 'data', 'data_type', 'scope', 'program', 'resolved_ip'
        ]
