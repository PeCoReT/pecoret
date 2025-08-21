from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core.mixins.object_lock import ObjectLockMixin
from backend.models.project_note import ProjectNote
from backend.api.serializers.project_note import ProjectNoteSerializer
from pecoret.core.utils.schema import extend_viewset_schema, extend_schema_view, extend_schema


@extend_viewset_schema(tags=['Projects'], verbose_name='project note')
@extend_schema_view(
    lock=extend_schema(tags=['Projects'], operation_id='Lock a project note'),
    unlock=extend_schema(tags=['Projects'], operation_id='Unlock a project note'),
)
class ProjectNoteViewSet(ObjectLockMixin, PeCoReTModelViewSet):
    queryset = ProjectNote.objects.none()
    search_fields = ['title', 'text']
    api_scope = 'scope_all_projects'
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]
    serializer_class = ProjectNoteSerializer

    def get_queryset(self):
        return ProjectNote.objects.for_project(self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project, current_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(current_user=self.request.user)
