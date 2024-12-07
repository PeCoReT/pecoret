from drf_spectacular.utils import extend_schema_view, extend_schema

from backend.api.serializers.asset import AssetSerializer
from backend.models import Asset
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import ModelViewSet


@extend_viewset_schema(tags=['Assets'], verbose_name=['asset'])
@extend_schema_view(
    custom_fields=extend_schema(operation_id='Custom Field list', tags=['Assets'])
)
class AssetViewSet(ModelViewSet):
    queryset = Asset.objects.none()
    filterset_class = None
    api_scope = 'scope_all_projects'
    search_fields = ['name']
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]
    serializer_class = AssetSerializer

    def get_queryset(self):
        return Asset.objects.for_project(self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project)
