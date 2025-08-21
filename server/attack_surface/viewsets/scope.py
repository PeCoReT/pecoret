from attack_surface.filters.scope import ScopeFilter
from attack_surface.mixins import ScanningAuthMixin
from attack_surface.permissions import ScanningPermission
from attack_surface.serializers.scope import ScopeSerializer
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet
from attack_surface.models import Scope
from pecoret.core import permissions


@extend_viewset_schema(tags=['Attack Surface'], verbose_name='scope')
class ScopeViewSet(ScanningAuthMixin, PeCoReTModelViewSet):
    queryset = Scope.objects.all()
    serializer_class = ScopeSerializer
    permission_classes = [
        # scanners should be allowed to fetch scope
        ScanningPermission(
            read_write_groups=[permissions.Groups.GROUP_PENTESTER],
            read_only_groups=[],
            scanner_read=True
        )
    ]
    api_scope = 'scope_attack_surface'
    search_fields = ['name']
    ordering_fields = ['date_created', 'date_updated']
    filterset_class = ScopeFilter
