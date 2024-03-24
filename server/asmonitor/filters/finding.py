from django_filters import rest_framework as filters
from pecoret.core.utils.filters import ChoiceFilter
from asmonitor.models.finding import Finding, Status, Severity


class FindingFilter(filters.FilterSet):
    status = ChoiceFilter(choices=Status.choices)
    severity = ChoiceFilter(choices=Severity.choices)

    class Meta:
        model = Finding
        fields = ['target', 'status', 'severity']
