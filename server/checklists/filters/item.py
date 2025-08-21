from django_filters import rest_framework as filters

from checklists.models import AssetItem, AssetCategory
from pecoret.core.utils.filters import filter_model_by_project


class AssetItemFilter(filters.FilterSet):
    category = filters.ModelChoiceFilter(
        field_name="category", queryset=filter_model_by_project(AssetCategory))

    class Meta:
        model = AssetItem
        fields = {
            "name": ["exact"]
        }
