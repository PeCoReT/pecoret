from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from attack_surface.filters.port import PortFilter
from attack_surface.mixins import ScanningAuthMixin
from attack_surface.permissions import ScanningPermission
from attack_surface.serializers.port import PortSerializer, Port
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet


@extend_viewset_schema(tags=['Attack Surface'], verbose_name='port')
@extend_schema_view(
    create_or_update=extend_schema(operation_id='Get or create a port', tags=['Attack Surface'])
)
class PortViewSet(ScanningAuthMixin, PeCoReTModelViewSet):
    queryset = Port.objects.all()
    serializer_class = PortSerializer
    permission_classes = [
        ScanningPermission(read_write_groups=[permissions.Groups.GROUP_PENTESTER], scanner_write=True,
                           scanner_read=True)
    ]
    api_scope = 'scope_attack_surface'
    search_fields = ['service_name', 'banner']
    ordering_fields = ['date_created', 'date_updated']
    filterset_class = PortFilter

    @action(detail=False, methods=["post"])
    def create_or_update(self, request, *args, **kwargs):
        qs = Port.objects.filter_unique(request.data['number'], request.data['protocol'], request.data['host'])
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
