from django_filters import rest_framework as filters
from django_filters import widgets

from advisories.models.advisory import Advisory, AdvisoryStatusChoices, VulnerabilityStatusChoices
from advisories.models.label import Label
from backend.models.vulnerability import Severity
from pecoret.core.utils.filters import ChoiceFilter


class AdvisoryFilter(filters.FilterSet):
    status = ChoiceFilter(choices=AdvisoryStatusChoices.choices)
    vulnerability_status = ChoiceFilter(choices=VulnerabilityStatusChoices.choices)
    severity = ChoiceFilter(choices=Severity.choices)
    # seems like `widgets.QueryArrayWidget` is required to have `labels[]=1` query syntax support
    labels = filters.ModelMultipleChoiceFilter(
        widget=widgets.QueryArrayWidget,
        queryset=Label.objects.all())

    class Meta:
        model = Advisory
        fields = ["status", "labels", "vulnerability_status", "severity", "technology"]
