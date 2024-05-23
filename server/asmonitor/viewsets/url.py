from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from asmonitor.mixins import TargetRelatedMixin
from asmonitor.models import URL
from asmonitor.permissions import ASMonitorGroupPermission
from asmonitor.serializers.url import URLSerializer, GlobalURLSerializer
from asmonitor.filters.url import URLFilter
from pecoret.core import permissions
from pecoret.core.mixins import ListModelMixin
from pecoret.core.viewsets import PeCoReTModelViewSet, GenericViewSet


class URLViewSet(TargetRelatedMixin, PeCoReTModelViewSet):
    queryset = URL.objects.none()
    serializer_class = URLSerializer
    search_fields = ['url', 'request', 'response']
    ordering_fields = ['date_updated', 'date_created', 'last_seen', 'status_code']
    filterset_class = URLFilter
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

    @action(detail=False, methods=["post"])
    def create_or_update(self, request, *args, **kwargs):
        serializer = URLSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        qs = URL.objects.filter_unique(request.data['url'], self.get_target())
        if qs.exists():
            serializer = self.get_serializer(qs.get(), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status.HTTP_200_OK)
        # create
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class GlobalURLViewSet(ListModelMixin, GenericViewSet):
    queryset = URL.objects.all()
    serializer_class = GlobalURLSerializer
    search_fields = ['url', 'request', 'response']
    filterset_class = URLFilter
    ordering_fields = ['date_updated', 'date_created', 'last_seen', 'status_code']
    api_scope = 'scope_asmonitor'
    permission_classes = [
        ASMonitorGroupPermission(
            read_write_groups=[
                permissions.Groups.GROUP_PENTESTER
            ]
        )
    ]
