from django_filters import rest_framework as filters, widgets

from pecoret.core.utils.filters import ChoiceFilter
from .base import ProgramFilterMixin
from ..models import Scope, ScopeItem, Program
from ..models.scoping.item import ScopeResult


class ScopeFilter(ProgramFilterMixin, filters.FilterSet):
    class Meta:
        model = Scope
        fields = [
            'program'
        ]


class ScopeItemFilter(filters.FilterSet):
    program = filters.ModelMultipleChoiceFilter(queryset=Program.objects.all(), field_name='scope__program',
                                                widget=widgets.QueryArrayWidget)
    domains_only = filters.BooleanFilter(method='filter_domains_only')
    scope = filters.ModelChoiceFilter(queryset=Scope.objects.all(), field_name='scope')
    results_in = ChoiceFilter(choices=ScopeResult.choices)

    class Meta:
        model = ScopeItem
        fields = [
            'domains_only',
            'program',
            'is_regex',
            'results_in'
        ]

    def filter_domains_only(self, queryset, name, value):
        if value is True:
            queryset = queryset.domains()
        return queryset
