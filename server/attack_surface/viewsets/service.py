from drf_spectacular.utils import extend_schema, extend_schema_view

from attack_surface.filters.service import ServiceFilter
from attack_surface.mixins import CreateOrUpdateMixin, ScanningAuthMixin, SearchQLMixin
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
class ServiceViewSet(CreateOrUpdateMixin, ScanningAuthMixin, SearchQLMixin, PeCoReTModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [
        ScanningPermission(read_write_groups=[], read_only_groups=[permissions.Groups.GROUP_PENTESTER],
                           scanner_write=True, scanner_read=True)
    ]
    api_scope = 'scope_attack_surface'
    search_fields = ['target__data']
    ordering_fields = ['date_created', 'date_updated']
    filterset_class = ServiceFilter

    def get_create_or_update_queryset(self, request):
        return Service.objects.filter_unique(request.data.get('port_number'), request.data.get('protocol'),
                                             request.data.get('target'))
