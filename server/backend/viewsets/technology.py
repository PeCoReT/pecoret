from drf_spectacular.utils import extend_schema_view, extend_schema
from backend.serializers.technology import TechnologySerializer
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from backend.models import Technology
from backend.filters.technology import TechnologyFilter


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
class TechnologyViewSet(PeCoReTModelViewSet):
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
