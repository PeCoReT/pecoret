from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from attack_surface.serializers.target import TargetSerializer, Target
from attack_surface.filters.target import TargetFilter


class TargetViewSet(PeCoReTModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[permissions.Groups.GROUP_PENTESTER],
            read_only_groups=[]
        )
    ]
    api_scope = 'scope_attack_surface'
    search_fields = ['data']
    ordering_fields = ['date_created', 'date_updated', 'first_seen', 'last_seen']
    filterset_class = TargetFilter
