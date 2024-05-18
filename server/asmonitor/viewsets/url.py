from asmonitor.mixins import TargetRelatedMixin
from asmonitor.models import URL
from asmonitor.permissions import ASMonitorGroupPermission
from asmonitor.serializers.url import URLSerializer, GlobalURLSerializer
from pecoret.core import permissions
from pecoret.core.mixins import ListModelMixin
from pecoret.core.viewsets import PeCoReTModelViewSet, GenericViewSet


class URLViewSet(TargetRelatedMixin, PeCoReTModelViewSet):
    queryset = URL.objects.none()
    serializer_class = URLSerializer
    search_fields = ['url', 'request', 'response']
    ordering_fields = ['date_updated', 'date_created', 'last_seen', 'status_code']
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
        return URL.objects.for_target(target)

    def perform_create(self, serializer):
        target = self.get_target()
        serializer.save(target=target)


class GlobalURLViewSet(ListModelMixin, GenericViewSet):
    queryset = URL.objects.all()
    serializer_class = GlobalURLSerializer
    search_fields = ['url', 'request', 'response']
    filterset_class = None
    ordering_fields = ['date_updated', 'date_created', 'last_seen', 'status_code']
    api_scope = 'scope_asmonitor'
    permission_classes = [
        ASMonitorGroupPermission(
            read_write_groups=[
                permissions.Groups.GROUP_PENTESTER
            ]
        )
    ]
