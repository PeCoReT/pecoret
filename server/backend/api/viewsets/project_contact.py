from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from backend.models.project_contact import ProjectContact
from backend.api.serializers.project_contact import ProjectContactSerializer
from pecoret.core.utils.schema import extend_viewset_schema


@extend_viewset_schema(tags=['Projects'], verbose_name='contact')
class ProjectContactViewSet(PeCoReTModelViewSet):
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]
    filterset_class = None
    api_scope = "scope_all_projects"
    search_fields = ["contact__first_name", "contact__last_name"]
    ordering_fields = ["date_created", "date_updated"]
    serializer_class = ProjectContactSerializer
    queryset = ProjectContact.objects.none()

    def get_queryset(self):
        return ProjectContact.objects.for_project(self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project)
