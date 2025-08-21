from django_filters import rest_framework as filters

from backend import models
from backend.models.finding import Finding, FindingStatus, Severity
from pecoret.core.utils.filters import ChoiceFilter, filter_model_by_project


class FindingFilter(filters.FilterSet):
    severity = ChoiceFilter(choices=Severity.choices)
    status = ChoiceFilter(choices=FindingStatus.choices)
    asset = filters.ModelChoiceFilter(field_name='asset', queryset=filter_model_by_project(models.Asset))

    class Meta:
        model = Finding
        fields = ["status", "severity", "needs_review"]
