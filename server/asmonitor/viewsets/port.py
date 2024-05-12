from rest_framework.exceptions import NotFound

from asmonitor.models import Host, Port
from asmonitor.permissions import ASMonitorGroupPermission
from asmonitor.serializers.port import PortSerializer
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet


class PortViewSet(PeCoReTModelViewSet):
    queryset = Port.objects.none()
    serializer_class = PortSerializer
    search_fields = ['port', 'protocol', 'banner', 'service']
    filterset_class = None
    api_scope = 'scope_asmonitor'
    permission_classes = [
        ASMonitorGroupPermission(
            read_write_groups=[
                permissions.Groups.GROUP_PENTESTER
            ]
        )
    ]

    def get_queryset(self):
        try:
            host = Host.objects.get(pk=self.kwargs.get('host'), program__pk=self.kwargs.get('program'))
        except Host.DoesNotExist:
            raise NotFound()
        return Port.objects.for_host(host)

    def perform_create(self, serializer):
        serializer.save(host_id=self.kwargs['host'])
