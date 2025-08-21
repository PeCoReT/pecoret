from pecoret.core.viewsets import PeCoReTReadOnlyModelViewSet, PeCoReTModelViewSet
from pecoret.core import permissions
from checklists.models import AssetCategory, Category
from checklists.serializers.category import CategorySerializer
from checklists.serializers.asset_category import AssetCategorySerializer
from checklists.filters.category import AssetCategoryFilter
from pecoret.core.utils.schema import extend_viewset_schema, extend_schema_view, extend_schema


@extend_schema_view(
    list=extend_schema(operation_id='Get all asset categories', tags=['Project Checklists']),
    retrieve=extend_schema(operation_id='Get specific category', tags=['Project Checklists']))
class AssetCategoryViewSet(PeCoReTReadOnlyModelViewSet):
    queryset = AssetCategory.objects.none()
    permission_classes = [
        permissions.PRESET_PENTESTER_OR_READONLY
    ]
    serializer_class = AssetCategorySerializer
    filterset_class = AssetCategoryFilter
    search_fields = ["name", "assetitem__name", "category_id"]
    api_scope = 'scope_all_projects'

    def get_queryset(self):
        return AssetCategory.objects.for_project(self.request.project)


@extend_viewset_schema(tags=['Checklists'], verbose_name='category', verbose_name_plural='categories')
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
