from attack_surface.mixins import ScanFeatureDispatchMixin, ScanningAuthMixin
from attack_surface.models import Scan
from attack_surface.permissions import ScanningPermission
from attack_surface.queue import enqueue_scan
from attack_surface.serializers.scanning.scan import ScanSerializer, ScanUpdateSerializer, ScannerScanUpdateSerializer
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet


@extend_viewset_schema(tags=['Attack Surface Scanning'], verbose_name='scan')
class ScanViewSet(ScanFeatureDispatchMixin, ScanningAuthMixin, PeCoReTModelViewSet):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer
    permission_classes = [
        ScanningPermission(read_write_groups=[permissions.Groups.GROUP_PENTESTER], scanner_write=True,
                           scanner_read=True)]
    search_fields = ['scan_id', 'name', 'scan_type__name']
    api_scope = 'scope_attack_surface'

    def get_serializer_class(self):
        if self.action in ['partial_update', 'update'] and self.request.headers.get('X-Scanner-Auth'):
            return ScannerScanUpdateSerializer
        elif self.action in ['partial_update', 'update']:
            return ScanUpdateSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        super().perform_create(serializer)
        enqueue_scan(serializer.data)
