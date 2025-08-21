from django_filters import rest_framework as filters

from attack_surface.models.finding_component import FindingComponent
from attack_surface.models.finding import Finding


class FindingComponentFilter(filters.FilterSet):
    finding = filters.ModelMultipleChoiceFilter(queryset=Finding.objects.all(), field_name='finding')

    class Meta:
        model = FindingComponent
        fields = ['finding']