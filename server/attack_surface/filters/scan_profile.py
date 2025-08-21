from django_filters import rest_framework as filters

from attack_surface.models.scanning import ScanProfile, ScanCategory


class ScanProfileFilter(filters.FilterSet):
    scan_category = filters.ModelChoiceFilter(queryset=ScanCategory.objects.all())

    class Meta:
        model = ScanProfile
        fields = [
            'scan_category',
        ]
