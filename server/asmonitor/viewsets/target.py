from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from asmonitor.filters.host import HostFilter
from asmonitor.models import Target
from asmonitor.permissions import ASMonitorGroupPermission
from asmonitor.serializers.target import TargetSerializer, GlobalTargetSerializer
from pecoret.core import permissions
from pecoret.core.mixins import ListModelMixin
from pecoret.core.viewsets import PeCoReTModelViewSet, GenericViewSet


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

    @action(detail=False, methods=["post"])
    def create_or_update(self, request, *args, **kwargs):
        serializer = TargetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        qs = Target.objects.filter(name=request.data.get('name'), ip=request.data.get('ip'))
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
