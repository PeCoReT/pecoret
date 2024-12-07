from django_filters import rest_framework as filters
from checklists.models import AssetChecklist


class AssetChecklistFilter(filters.FilterSet):


    class Meta:
        model = AssetChecklist
        fields = {
            "checklist_id": ["exact"]
        }
