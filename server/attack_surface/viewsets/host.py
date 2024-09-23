from attack_surface.mixins import CreateOrUpdateMixin, ScanningAuthMixin
from attack_surface.models import Host
from attack_surface.permissions import ScanningPermission
from attack_surface.serializers.host import HostSerializer
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet


@extend_viewset_schema(tags=['Attack Surface'], verbose_name='host')
class HostViewSet(CreateOrUpdateMixin, ScanningAuthMixin, PeCoReTModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    permission_classes = [
        ScanningPermission(read_write_groups=[permissions.Groups.GROUP_PENTESTER], scanner_write=True,
                           scanner_read=True)
    ]
    ordering_fields = ['date_asn_last_updated', 'date_updated']
    api_scope = 'scope_attack_surface'

    def get_create_or_update_queryset(self, request):
        return Host.objects.filter_unique(request.data['ip_address'])
