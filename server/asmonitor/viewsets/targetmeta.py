from rest_framework.exceptions import NotFound

from asmonitor.models import TargetMeta, Host
from asmonitor.permissions import ASMonitorGroupPermission
from asmonitor.serializers.targetmeta import TargetMetaSerializer
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet


class TargetMetaViewSet(PeCoReTModelViewSet):
    queryset = TargetMeta.objects.none()
    serializer_class = TargetMetaSerializer
    search_fields = ['key', 'value']
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
        return TargetMeta.objects.for_host(host)

    def perform_create(self, serializer):
        serializer.save(host_id=self.kwargs['host'])
