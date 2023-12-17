from pecoret.core.viewsets import PeCoReTReadOnlyModelViewSet, PeCoReTNoUpdateViewSet, PeCoReTModelViewSet
from pecoret.core import permissions
from checklists.models import Checklist, AssetChecklist
from checklists.serializers.checklist import (
    ChecklistSerializer,
    AssetChecklistSerializer,
    AssetChecklistCreateSerializer,
)
from checklists.filters.checklists import AssetChecklistFilter


class ChecklistViewSet(PeCoReTModelViewSet):
    queryset = Checklist.objects.none()
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[
                permissions.Groups.GROUP_PENTESTER
            ],
            read_only_groups=[
                permissions.Groups.GROUP_MANAGEMENT
            ]
        )
    ]
    search_fields = ["name", "checklist_id"]
    serializer_class = ChecklistSerializer

    def get_queryset(self):
        return Checklist.objects.all()


class AssetChecklistViewSet(PeCoReTNoUpdateViewSet):
    queryset = AssetChecklist.objects.none()
    filterset_class = AssetChecklistFilter
    search_fields = ["name"]
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]
    serializer_class = AssetChecklistSerializer

    def get_queryset(self):
        return AssetChecklist.objects.for_project(self.request.project)

    def get_serializer_class(self):
        if self.action == "create":
            return AssetChecklistCreateSerializer
        return AssetChecklistSerializer

    def perform_create(self, serializer):
        serializer.save(project=self.request.project)

    def perform_destroy(self, instance):
        instance.categories.all().delete()
        super().perform_destroy(instance)
