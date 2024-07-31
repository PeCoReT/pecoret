from pecoret.core.viewsets import PeCoReTNoUpdateViewSet, PeCoReTModelViewSet
from pecoret.core import permissions
from checklists.models import Checklist, AssetChecklist
from checklists.serializers.checklist import (
    ChecklistSerializer,
    AssetChecklistSerializer,
    AssetChecklistCreateSerializer,
)
from checklists.filters.checklists import AssetChecklistFilter
from pecoret.core.utils.schema import extend_viewset_schema, extend_schema_view, extend_schema


@extend_viewset_schema(tags=['Checklists'], verbose_name='checklist')
class ChecklistViewSet(PeCoReTModelViewSet):
    queryset = Checklist.objects.none()
    api_scope = 'scope_knowledgebase'
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


@extend_schema_view(
    list=extend_schema(operation_id='Get all asset checklists', tags=['Project Checklists']),
    retrieve=extend_schema(operation_id='Get specific asset checklist', tags=['Project Checklists']),
    destroy=extend_schema(operation_id='Delete a asset checklist', tags=['Project Checklists']),
    create=extend_schema(operation_id='Create a new asset checklist', tags=['Project Checklists']),
)
class AssetChecklistViewSet(PeCoReTNoUpdateViewSet):
    queryset = AssetChecklist.objects.none()
    filterset_class = AssetChecklistFilter
    search_fields = ["name"]
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]
    serializer_class = AssetChecklistSerializer
    api_scope = 'scope_all_projects'

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
