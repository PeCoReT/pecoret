from attack_surface.mixins import CreateOrUpdateMixin
from attack_surface.permissions import ScanningPermission
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet
from attack_surface.serializers.tag import TagSerializer, Tag
from pecoret.core.utils.schema import extend_viewset_schema


@extend_viewset_schema(tags=['Attack Surface'], verbose_name='tag')
class TagViewSet(CreateOrUpdateMixin, PeCoReTModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [
        ScanningPermission(read_write_groups=[permissions.Groups.GROUP_PENTESTER], scanner_write=True,
                           scanner_read=True)
    ]
    api_scope = 'scope_attack_surface'
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    filterset_class = None

    def get_create_or_update_queryset(self, request):
        return Tag.objects.filter(name=request.data['name'])
