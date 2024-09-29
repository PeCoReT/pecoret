from attack_surface.mixins import ScanFeatureDispatchMixin
from attack_surface.models import ScanType
from attack_surface.serializers.scanning.scan_type import ScanTypeSerializer
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet


@extend_viewset_schema(tags=['Attack Surface Scanning'], verbose_name='scan type')
class ScanTypeViewSet(ScanFeatureDispatchMixin, PeCoReTModelViewSet):
    queryset = ScanType.objects.all()
    serializer_class = ScanTypeSerializer
    permission_classes = [
        permissions.GroupPermission(read_only_groups=[permissions.Groups.GROUP_PENTESTER], read_write_groups=[])]
    search_fields = ['name']
    api_scope = 'scope_attack_surface'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ScanType.objects.all()
        return ScanType.objects.enabled()
