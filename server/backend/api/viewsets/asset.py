from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.api.serializers.custom_field_asset import CustomFieldAssetSerializer
from backend.models import Asset, CustomFieldAsset
from pecoret.core.viewsets import ModelViewSet
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core import permissions
from backend.api.serializers.asset import AssetSerializer


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

    @action(detail=False, methods=['get'], serializer_class=CustomFieldAssetSerializer)
    def custom_fields(self, *args, **kwargs):
        queryset = self.filter_queryset(CustomFieldAsset.objects.all())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CustomFieldAssetSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CustomFieldAssetSerializer(queryset, many=True)
        return Response(serializer.data)
