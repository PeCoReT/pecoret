from pecoret.core.viewsets import PeCoReTModelViewSet, GenericViewSet
from pecoret.core.mixins import ListModelMixin
from pecoret.core import permissions
from asmonitor.permissions import ASMonitorGroupPermission
from asmonitor.models import Target
from asmonitor.filters.host import HostFilter
from asmonitor.serializers.target import TargetSerializer, GlobalTargetSerializer


class TargetViewSet(PeCoReTModelViewSet):
    queryset = Target.objects.none()
    serializer_class = TargetSerializer
    search_fields = ['ip', 'description', 'name']
    ordering_fields = ['ip', 'date_updated', 'date_created', 'last_seen', 'name']
    filterset_class = HostFilter
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


class GlobalTargetViewSet(ListModelMixin, GenericViewSet):
    queryset = Target.objects.all()
    serializer_class = GlobalTargetSerializer
    search_fields = ['ip', 'description', 'name', 'targetmeta__key']
    ordering_fields = ['ip', 'date_updated', 'date_created', 'last_seen']
    filterset_class = HostFilter
    api_scope = 'scope_asmonitor'
    permission_classes = [
        ASMonitorGroupPermission(
            read_write_groups=[
                permissions.Groups.GROUP_PENTESTER
            ]
        )
    ]
