from backend.serializers.technology import TechnologySerializer
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from backend.models import Technology


class TechnologyViewSet(PeCoReTModelViewSet):
    queryset = Technology.objects.all()
    search_fields = ['cpe', 'name']
    api_scope = 'scope_misc'
    serializer_class = TechnologySerializer
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[
                permissions.Groups.GROUP_PENTESTER
            ],
            read_only_groups=[]
        )
    ]