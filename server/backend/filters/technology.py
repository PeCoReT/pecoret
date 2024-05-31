from django_filters import rest_framework as filters
from backend.models.technology import Technology


class SourceCodeFilter(filters.BooleanFilter):
    def filter(self, qs, value):
        return qs.with_source_code(value)


class TechnologyFilter(filters.FilterSet):
    source_code_available = SourceCodeFilter()

    class Meta:
        model = Technology
        fields = ['source_code_available', 'cpe', 'name', 'vendor']
