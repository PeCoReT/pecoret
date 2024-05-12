from rest_framework.exceptions import NotFound
from asmonitor.models import Hostname, Host
from asmonitor.permissions import ASMonitorGroupPermission
from asmonitor.serializers.hostname import HostnameSerializer
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet


class HostnameViewSet(PeCoReTModelViewSet):
    queryset = Hostname.objects.none()
    serializer_class = HostnameSerializer
    search_fields = ['name']
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
        return Hostname.objects.for_host(host)

    def perform_create(self, serializer):
        serializer.save(host_id=self.kwargs['host'])
