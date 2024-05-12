from rest_framework.exceptions import NotFound
from pecoret.core.mixins import ListModelMixin
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet, GenericViewSet
from asmonitor.models import URL, Host
from asmonitor.permissions import ASMonitorGroupPermission
from asmonitor.serializers.url import URLSerializer, GlobalURLSerializer


class URLViewSet(PeCoReTModelViewSet):
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
        try:
            host = Host.objects.get(pk=self.kwargs.get('host'), program__pk=self.kwargs.get('program'))
        except Host.DoesNotExist:
            raise NotFound()
        return URL.objects.for_host(host)

    def perform_create(self, serializer):
        serializer.save(host_id=self.kwargs['host'])


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
