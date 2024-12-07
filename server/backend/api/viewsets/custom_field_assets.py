from backend.api.filters.custom_field_asset import CustomFieldAssetFilter
from backend.api.serializers.asset import CustomFieldAssetSerializer
from backend.models import CustomFieldAsset
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import GenericViewSet
from pecoret.core.mixins import RetrieveModelMixin, ListModelMixin


@extend_viewset_schema(tags=['Assets'], verbose_name=['custom-field-asset'])
class CustomFieldAssetViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = CustomFieldAsset.objects.all()
    filterset_class = CustomFieldAssetFilter
    api_scope = 'scope_knowledgebase'
    search_fields = ['name']
    permission_classes = [permissions.GroupPermission(
        read_only_groups=[permissions.Groups.GROUP_PENTESTER, permissions.Groups.GROUP_MANAGEMENT])]
    serializer_class = CustomFieldAssetSerializer
