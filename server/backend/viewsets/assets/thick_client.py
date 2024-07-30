from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from backend.models.assets.thick_client import ThickClient
from backend.serializers.assets.thick_client import ThickClientSerializer


@extend_viewset_schema(tags=['Projects'], verbose_name='thick client asset')
class ThickClientViewSet(PeCoReTModelViewSet):
    permission_classes = [
        permissions.PRESET_PENTESTER_OR_READONLY
    ]
    api_scope = "scope_all_projects"
    queryset = ThickClient.objects.none()
    serializer_class = ThickClientSerializer
    filterset_class = None
    search_fields = ["name"]
    ordering_fields = ["name", "date_created", "date_updated"]

    def get_queryset(self):
        return ThickClient.objects.for_project(self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project)
