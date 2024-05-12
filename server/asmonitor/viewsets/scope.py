from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from asmonitor.permissions import ASMonitorGroupPermission
from asmonitor.models.scope import Scope
from asmonitor.serializers.scope import ScopeSerializer


class ScopeViewSet(PeCoReTModelViewSet):
    queryset = Scope.objects.none()
    serializer_class = ScopeSerializer
    search_fields = ['data']
    ordering_fields = ['date_updated', 'date_created']
    filterset_class = None
    api_scope = 'scope_asmonitor'
    permission_classes = [
        ASMonitorGroupPermission(
            read_write_groups=[
                permissions.Groups.GROUP_PENTESTER
            ]
        )
    ]

    def perform_create(self, serializer):
        serializer.save(program=self.request.program)

    def get_queryset(self):
        return Scope.objects.for_program(self.request.program)
