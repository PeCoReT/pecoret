import base64
import time

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from attack_surface.filters.service import ServiceFilter
from attack_surface.mixins import CreateOrUpdateMixin, ScanningAuthMixin
from attack_surface.models import Service
from attack_surface.permissions import ScanningPermission
from attack_surface.serializers.service import ServiceSerializer
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet


@extend_viewset_schema(tags=['Attack Surface'], verbose_name='service')
@extend_schema_view(
    search=extend_schema(operation_id='Search services and nested items', tags=['Attack Surface'])
)
class ServiceViewSet(CreateOrUpdateMixin, ScanningAuthMixin, PeCoReTModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [
        ScanningPermission(read_write_groups=[permissions.Groups.GROUP_PENTESTER], scanner_write=True,
                           scanner_read=True)
    ]
    api_scope = 'scope_attack_surface'
    search_fields = ['target__data']
    ordering_fields = ['date_created', 'date_updated']
    filterset_class = ServiceFilter

    @action(detail=False, methods=['get'])
    def search(self, request, *args, **kwargs):
        qs = self.get_queryset()
        if request.GET.get('search'):
            try:
                data = base64.b64decode(request.GET.get('search').encode())
                qs = qs.djangoql(data.decode())
            except Exception as e:
                print(e)
                return Response({'search': 'Error processing search'}, status=status.HTTP_400_BAD_REQUEST)
        if request.GET.get('download'):
            import json
            serializer = self.get_serializer(qs, many=True)
            response = Response(json.dumps(serializer.data), content_type='application/json')
            filename = f'search-results-{int(time.time())}.json'
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def get_create_or_update_queryset(self, request):
        return Service.objects.filter_unique(request.data.get('port_number'), request.data.get('protocol'),
                                             request.data.get('target'))
