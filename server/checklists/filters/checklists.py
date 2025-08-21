from django_filters import rest_framework as filters
from checklists.models import AssetChecklist
from backend.models import Asset
from pecoret.core.utils.filters import filter_model_by_project


class AssetChecklistFilter(filters.FilterSet):
    asset = filters.ModelChoiceFilter(field_name='asset', queryset=filter_model_by_project(Asset))

    class Meta:
        model = AssetChecklist
        fields = {
            "checklist_id": ["exact"]
        }
