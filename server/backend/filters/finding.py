from django_filters import rest_framework as filters

from backend import models
from backend.models.finding import Finding, FindingStatus, Severity
from pecoret.core.utils.filters import ChoiceFilter, filter_model_by_project


class FindingFilter(filters.FilterSet):
    severity = ChoiceFilter(choices=Severity.choices)
    status = ChoiceFilter(choices=FindingStatus.choices)
    web_application = filters.ModelChoiceFilter(field_name="web_application",
                                                queryset=filter_model_by_project(models.WebApplication))
    host = filters.ModelChoiceFilter(field_name="host", queryset=filter_model_by_project(models.Host))
    service = filters.ModelChoiceFilter(field_name="service", queryset=filter_model_by_project(models.Service))
    mobile_application = filters.ModelChoiceFilter(field_name='mobile_application',
                                                   queryset=filter_model_by_project(models.MobileApplication))
    thick_client = filters.ModelChoiceFilter(field_name='thick_client',
                                             queryset=filter_model_by_project(models.ThickClient))

    class Meta:
        model = Finding
        fields = ["status", "severity", "needs_review"]
