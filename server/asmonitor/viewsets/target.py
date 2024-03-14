from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from asmonitor.permissions import ASMonitorGroupPermission
from asmonitor.models import Target
from asmonitor.filters.target import TargetFilter
from asmonitor.serializers.target import TargetSerializer


class TargetViewSet(PeCoReTModelViewSet):
    queryset = Target.objects.none()
    serializer_class = TargetSerializer
    search_fields = ['name', 'ip']
    ordering_fields = ['name', 'date_updated', 'date_created', 'last_seen']
    filterset_class = TargetFilter
    api_scope = 'scope_asmonitor'
    permission_classes = [
        ASMonitorGroupPermission(
            read_write_groups=[
                permissions.Groups.GROUP_PENTESTER
            ]
        )
    ]

    def get_queryset(self):
        return Target.objects.for_program(self.request.program)

    def perform_create(self, serializer):
        serializer.save(program=self.request.program)
