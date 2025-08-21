from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from backend.models import ProjectScope
from backend.api.serializers.project_scope import ProjectScopeSerializer
from pecoret.core.utils.schema import extend_viewset_schema


@extend_viewset_schema(tags=['Projects'], verbose_name='project scope')
class ProjectScopeViewSet(PeCoReTModelViewSet):
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]
    filterset_class = None
    api_scope = "scope_all_projects"
    search_fields = ["details"]
    serializer_class = ProjectScopeSerializer
    queryset = ProjectScope.objects.none()

    def get_queryset(self):
        return ProjectScope.objects.for_project(self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project)
