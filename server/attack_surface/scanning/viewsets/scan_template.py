from attack_surface.scanning.models import ScanTemplate
from attack_surface.scanning.serializers.scan_template import MinimalScanTemplateSerializer
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTReadOnlyModelViewSet


@extend_viewset_schema(tags=['Attack Surface Scanning'], verbose_name='scan batch request')
class ScanTemplateViewSet(PeCoReTReadOnlyModelViewSet):
    serializer_class = MinimalScanTemplateSerializer
    queryset = ScanTemplate.objects.all()
    permission_classes = [
        permissions.GroupPermission(read_write_groups=[permissions.Groups.GROUP_PENTESTER], read_only_groups=[])
    ]
    api_scope = 'scope_attack_surface'
    search_fields = ['name']
