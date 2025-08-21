from django_filters import rest_framework as filters
from backend.models.cwe import CWE


class CWEFilter(filters.FilterSet):

    class Meta:
        model = CWE
        fields = ["cwe_id"]
