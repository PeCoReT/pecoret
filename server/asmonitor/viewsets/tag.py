from asmonitor.models import Tag
from asmonitor.serializers.tag import TagSerializer
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet


class TagViewSet(PeCoReTModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.GroupPermission(
        read_write_groups=[permissions.Groups.GROUP_PENTESTER],
        read_only_groups=[]
    )]
    api_scope = 'scope_asmonitor'
    search_fields = ['name', 'description']
