from attack_surface.mixins import CreateOrUpdateMixin, ScanningAuthMixin
from attack_surface.models import ASN
from attack_surface.permissions import ScanningPermission
from attack_surface.serializers.asn import ASNSerializer
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet


class ASNViewSet(CreateOrUpdateMixin, ScanningAuthMixin, PeCoReTModelViewSet):
    queryset = ASN.objects.all()
    serializer_class = ASNSerializer
    permission_classes = [
        ScanningPermission(read_write_groups=[], read_only_groups=[permissions.Groups.GROUP_PENTESTER],
                           scanner_write=True, scanner_read=True)
    ]
    ordering_fields = ['name', 'date_updated', 'date_created']
    api_scope = 'scope_attack_surface'

    def get_create_or_update_queryset(self, request):
        return ASN.objects.filter_unique(request.data['value'])
