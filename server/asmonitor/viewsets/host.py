from pecoret.core.viewsets import PeCoReTModelViewSet, GenericViewSet
from pecoret.core.mixins import ListModelMixin
from pecoret.core import permissions
from asmonitor.permissions import ASMonitorGroupPermission
from asmonitor.models import Host
from asmonitor.filters.host import HostFilter
from asmonitor.serializers.host import HostSerializer, GlobalHostSerializer


class HostViewSet(PeCoReTModelViewSet):
    queryset = Host.objects.none()
    serializer_class = HostSerializer
    search_fields = ['ip', 'description', 'hostname__name']
    ordering_fields = ['ip', 'date_updated', 'date_created', 'last_seen', 'hostname__name']
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
        return Host.objects.for_program(self.request.program)

    def perform_create(self, serializer):
        serializer.save(program=self.request.program)


class GlobalHostViewSet(ListModelMixin, GenericViewSet):
    queryset = Host.objects.all()
    serializer_class = GlobalHostSerializer
    search_fields = ['ip', 'description', 'hostname__name', 'targetmeta__key']
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
