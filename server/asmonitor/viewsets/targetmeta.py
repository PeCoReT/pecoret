from asmonitor.mixins import TargetRelatedMixin
from asmonitor.models import TargetMeta
from asmonitor.permissions import ASMonitorGroupPermission
from asmonitor.serializers.targetmeta import TargetMetaSerializer
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet


class TargetMetaViewSet(TargetRelatedMixin, PeCoReTModelViewSet):
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
        target = self.get_target()
        return TargetMeta.objects.for_target(target)

    def perform_create(self, serializer):
        target = self.get_target(validation_error=True)
        serializer.save(target=target)
