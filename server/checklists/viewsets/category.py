from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from pecoret.core.viewsets import PeCoReTReadOnlyModelViewSet, PeCoReTModelViewSet
from pecoret.core import permissions
from checklists.models import AssetCategory, Category
from checklists.serializers.category import AssetCategorySerializer, CategorySerializer
from checklists.filters.category import AssetCategoryFilter


class AssetCategoryViewSet(PeCoReTReadOnlyModelViewSet):
    queryset = AssetCategory.objects.none()
    permission_classes = [
        permissions.PRESET_PENTESTER_OR_READONLY
    ]
    serializer_class = AssetCategorySerializer
    filterset_class = AssetCategoryFilter
    search_fields = ["name", "assetitem__name"]

    def get_queryset(self):
        return AssetCategory.objects.for_project(self.request.project)


class CategoryViewSet(PeCoReTModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[
                permissions.Groups.GROUP_PENTESTER
            ],
            read_only_groups=[
                permissions.Groups.GROUP_MANAGEMENT
            ]
        )
    ]
    search_fields = ['name', 'category_id']
    serializer_class = CategorySerializer
