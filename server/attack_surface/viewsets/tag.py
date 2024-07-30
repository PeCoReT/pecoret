from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet
from attack_surface.serializers.tag import TagSerializer, Tag
from pecoret.core.utils.schema import extend_viewset_schema


@extend_viewset_schema(tags=['Attack Surface'], verbose_name='tag')
class TagViewSet(PeCoReTModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[permissions.Groups.GROUP_PENTESTER],
            read_only_groups=[]
        )
    ]
    api_scope = 'scope_attack_surface'
    search_fields = ['name', 'description']
    ordering_fields = ['name']
    filterset_class = None
