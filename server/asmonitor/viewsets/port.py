from asmonitor.models import Port
from asmonitor.permissions import ASMonitorGroupPermission
from asmonitor.serializers.port import PortSerializer
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet
from asmonitor.mixins import TargetRelatedMixin


class PortViewSet(TargetRelatedMixin, PeCoReTModelViewSet):
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
        target = self.get_target()
        return Port.objects.for_target(target)

    def perform_create(self, serializer):
        target = self.get_target(validation_error=True)
        serializer.save(target=target)
