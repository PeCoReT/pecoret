from django_filters import rest_framework as filters
from pecoret.core.utils.filters import ChoiceFilter

from attack_surface.models.scanning import Scan, ScanTask
from attack_surface.models.scanning.scan_task import ScanStatus


class ScanTaskFilter(filters.FilterSet):
    scan = filters.ModelChoiceFilter(queryset=Scan.objects.all())
    status = ChoiceFilter(choices=ScanStatus.choices)

    class Meta:
        model = ScanTask
        fields = [
            'scan', 'status',
        ]
