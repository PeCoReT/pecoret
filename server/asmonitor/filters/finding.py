from django_filters import rest_framework as filters
from django_filters import widgets
from pecoret.core.utils.filters import ChoiceFilter
from asmonitor.models.finding import Finding, Status, Severity
from asmonitor.models import Tag


class FindingFilter(filters.FilterSet):
    status = ChoiceFilter(choices=Status.choices)
    severity = ChoiceFilter(choices=Severity.choices)
    tags = filters.ModelMultipleChoiceFilter(
        widget=widgets.QueryArrayWidget, queryset=Tag.objects.all())

    class Meta:
        model = Finding
        fields = ['host', 'status', 'severity', 'tags']
