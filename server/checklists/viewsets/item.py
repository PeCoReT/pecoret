from checklists.models import AssetItem, Item
from checklists.serializers.item import AssetItemSerializer, AssetItemUpdateSerializer, ItemSerializer
from checklists.filters.item import AssetItemFilter
from pecoret.core.viewsets import PeCoReTNoDestroyViewSet, PeCoReTModelViewSet
from pecoret.core import permissions


class AssetItemViewSet(PeCoReTNoDestroyViewSet):
    queryset = AssetItem.objects.none()
    permission_classes = [
        permissions.PRESET_PENTESTER_OR_READONLY
    ]
    serializer_class = AssetItemSerializer
    filterset_class = AssetItemFilter
    api_scope = 'scope_all_projects'
    search_fields = ["name"]

    def get_queryset(self):
        return AssetItem.objects.for_project(self.request.project)

    def get_serializer_class(self):
        if self.action in ["patch", "put"]:
            return AssetItemUpdateSerializer
        return AssetItemSerializer


class ItemViewSet(PeCoReTModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    search_fields = ['name', 'item_id']
    api_scope = 'scope_misc'
    permission_classes = [
        permissions.GroupPermission(
            read_only_groups=[
                permissions.Groups.GROUP_MANAGEMENT
            ],
            read_write_groups=[
                permissions.Groups.GROUP_PENTESTER
            ]
        )
    ]
