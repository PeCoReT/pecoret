from backend.api.serializers.asset_type import AssetTypeSerializer
from backend.models import AssetType
from pecoret.core.mixins import ListModelMixin, RetrieveModelMixin
from pecoret.core.viewsets import GenericViewSet
from pecoret.core import permissions


class AssetTypeViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [
        permissions.GroupPermission(read_only_groups=[
            permissions.Groups.GROUP_PENTESTER,
            permissions.Groups.GROUP_MANAGEMENT
        ], read_write_groups=[])
    ]
    queryset = AssetType.objects.all()
    filterset_class = None
    search_fields = ['name']
    api_scope = 'scope_knowledgebase'
    serializer_class = AssetTypeSerializer
