from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet
from backend.models.project_note import ProjectNote
from backend.serializers.project_note import ProjectNoteSerializer


class ProjectNoteViewSet(PeCoReTModelViewSet):
    queryset = ProjectNote.objects.none()
    search_fields = ['title', 'text']
    api_scope = 'scope_all_projects'
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]
    serializer_class = ProjectNoteSerializer

    def get_queryset(self):
        return ProjectNote.objects.for_project(self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project)
