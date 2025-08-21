from drf_spectacular.utils import extend_schema_view, extend_schema

from attack_surface.filters.target import TargetFilter
from attack_surface.mixins import CreateOrUpdateMixin, ScanningAuthMixin
from attack_surface.permissions import ScanningPermission
from attack_surface.serializers.target import TargetSerializer, Target
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet


@extend_viewset_schema(tags=['Attack Surface'], verbose_name='target')
@extend_schema_view(
    create_or_update=extend_schema(operation_id='Get or create a target', tags=['Attack Surface'])
)
class TargetViewSet(CreateOrUpdateMixin, ScanningAuthMixin, PeCoReTModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    permission_classes = [
        ScanningPermission(read_write_groups=[], read_only_groups=[permissions.Groups.GROUP_PENTESTER],
                           scanner_write=True, scanner_read=True)

    ]
    api_scope = 'scope_attack_surface'
    search_fields = ['data']
    ordering_fields = ['date_created', 'date_updated']
    filterset_class = TargetFilter

    def get_create_or_update_queryset(self, request):
        return Target.objects.filter_unique(request.data['data'], request.data['program'])
 