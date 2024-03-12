from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet
from asmonitor.serializers.program import ProgramSerializer
from asmonitor.models import Program


class ProgramViewSet(PeCoReTModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[
                permissions.Groups.GROUP_PENTESTER
            ],
            read_only_groups=[]
        )
    ]
    api_scope = 'scope_asmonitor'
    search_fields = ['name', 'description']
