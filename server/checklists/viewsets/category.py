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
    api_scope = 'scope_all_projects'

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
    api_scope = 'scope_knowledgebase'
    search_fields = ['name', 'category_id']
    serializer_class = CategorySerializer
