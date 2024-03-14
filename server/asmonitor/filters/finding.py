from django_filters import rest_framework as filters
from asmonitor.models import Finding


class FindingFilter(filters.FilterSet):
    class Meta:
        model = Finding
        fields = ['target']
