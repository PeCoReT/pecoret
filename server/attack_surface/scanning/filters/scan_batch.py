from django_filters import rest_framework as filters

from attack_surface.scanning.models import ScanBatchRequest
from attack_surface.scanning.models.scan_batch import StatusChoices
from pecoret.core.utils.filters import ChoiceFilter


class ScanBatchRequestFilter(filters.FilterSet):
    status = ChoiceFilter(choices=StatusChoices.choices)

    class Meta:
        model = ScanBatchRequest
        fields = [
            'status',
        ]
