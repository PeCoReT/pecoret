from pecoret.core.viewsets import PeCoReTModelViewSet
from attack_surface.models.program import Program
from attack_surface.serializers.program import ProgramSerializer
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema


@extend_viewset_schema(tags=['Attack Surface'], verbose_name='program')
class ProgramViewSet(PeCoReTModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[permissions.Groups.GROUP_PENTESTER],
            read_only_groups=[]
        )
    ]
    api_scope = 'scope_attack_surface'
    search_fields = ['name', 'description']
    ordering_fields = ['date_created', 'date_updated', 'name']
    filterset_class = None
