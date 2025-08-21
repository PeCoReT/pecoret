from django_filters import rest_framework as filters
from checklists.models import AssetCategory, AssetChecklist
from pecoret.core.utils.filters import filter_model_by_project


class AssetCategoryFilter(filters.FilterSet):
    checklist = filters.ModelChoiceFilter(
        field_name="assetchecklist", queryset=filter_model_by_project(AssetChecklist))

    class Meta:
        model = AssetCategory
        fields = {
            "name": ["exact"]
        }
