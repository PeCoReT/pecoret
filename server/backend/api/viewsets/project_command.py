from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from backend.models.project_command import ProjectCommand
from backend.api.serializers.project_command import ProjectCommandSerializer
from pecoret.core.utils.schema import extend_viewset_schema


@extend_viewset_schema(tags=['Projects'], verbose_name='command')
class ProjectCommandViewSet(PeCoReTModelViewSet):
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]
    filterset_class = None
    api_scope = "scope_all_projects"
    search_fields = ["command", "output"]
    ordering_fields = ["date_run"]
    serializer_class = ProjectCommandSerializer
    queryset = ProjectCommand.objects.none()

    def get_queryset(self):
        return ProjectCommand.objects.for_project(self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project, user=self.request.user)
