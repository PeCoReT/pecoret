from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action

from attack_surface.authentication import ScannerAuth
from attack_surface.mixins import CreateOrUpdateMixin
from attack_surface.permissions import ScanningPermission
from backend.api.filters.technology import TechnologyFilter
from backend.models import Technology
from backend.api.serializers.technology import TechnologySerializer
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet


@extend_schema_view(
    list=extend_schema(
        operation_id='Get all technologies', tags=['Technologies']
    ),
    create=extend_schema(
        operation_id='Create a new technology', tags=['Technologies']
    ),
    retrieve=extend_schema(
        operation_id='Get a specific technology', tags=['Technologies']
    ),
    destroy=extend_schema(
        operation_id='Delete a technology', tags=['Technologies']
    ),
    partial_update=extend_schema(
        operation_id='Partially update a technology', tags=['Technologies']
    ),
    update=extend_schema(
        operation_id='Update a technology', tags=['Technologies']
    )
)
class TechnologyViewSet(CreateOrUpdateMixin, PeCoReTModelViewSet):
    queryset = Technology.objects.all()
    search_fields = ['cpe', 'name']
    api_scope = 'scope_knowledgebase'
    serializer_class = TechnologySerializer
    filterset_class = TechnologyFilter
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[
                permissions.Groups.GROUP_PENTESTER
            ],
            read_only_groups=[]
        )
    ]

    def get_create_or_update_queryset(self, request):
        return Technology.objects.filter(cpe=request.data.get('cpe'))

    @action(detail=False, methods=['post'], authentication_classes=[ScannerAuth],
            permission_classes=[ScanningPermission(scanner_read=True, scanner_write=True)])
    def create_or_update(self, request, *args, **kwargs):
        # allow scanner to create or update technology
        return super().create_or_update(request, *args, **kwargs)
