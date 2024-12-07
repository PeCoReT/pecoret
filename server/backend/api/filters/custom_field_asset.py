from django_filters import rest_framework as filters
from backend.models import CustomFieldAsset, AssetType


class CustomFieldAssetFilter(filters.FilterSet):
    asset_type = filters.ModelChoiceFilter(
        method='asset_type_filter',
        queryset=AssetType.objects.all(),
    )

    def asset_type_filter(self, queryset, name, value):
        return queryset.for_asset_type(value)

    class Meta:
        model = CustomFieldAsset
        fields = ['asset_type']
