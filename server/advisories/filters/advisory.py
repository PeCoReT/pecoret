from django_filters import rest_framework as filters
from backend.models.advisory import Advisory, AdvisoryStatusChoices
from pecoret.core.utils.filters import ChoiceFilter


class AdvisoryFilter(filters.FilterSet):
    status = ChoiceFilter(choices=AdvisoryStatusChoices.choices)

    class Meta:
        model = Advisory
        fields = ["status"]
