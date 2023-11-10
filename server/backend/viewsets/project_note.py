from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core.mixins.object_lock import ObjectLockMixin
from backend.models.project_note import ProjectNote
from backend.serializers.project_note import ProjectNoteSerializer


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
