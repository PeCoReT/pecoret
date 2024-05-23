from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(detail=False, methods=["post"])
    def create_or_update(self, request, *args, **kwargs):
        serializer = PortSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        qs = Port.objects.filter_unique(request.data['protocol'], request.data['port'], self.get_target())
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
