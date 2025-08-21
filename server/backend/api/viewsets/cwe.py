from drf_spectacular.utils import extend_schema_view, extend_schema

from backend.api.serializers.cwe import CWESerializer
from backend.models.cwe import CWE
from backend.api.filters.cwe import CWEFilter
from pecoret.core.viewsets import PeCoReTReadOnlyModelViewSet
from pecoret.core import permissions


@extend_schema_view(
    list=extend_schema(
        operation_id='Get all CWEs', tags=['CWEs']
    ),
    retrieve=extend_schema(
        operation_id='Get a specific CWE', tags=['CWEs']
    )
)
class CWEViewSet(PeCoReTReadOnlyModelViewSet):
    serializer_class = CWESerializer
    permission_classes = [
        permissions.PRESET_GROUP_SUPERUSER_OR_READ_ONLY
    ]
    queryset = CWE.objects.all()
    search_fields = ["cwe_id", "name"]
    filterset_class = CWEFilter
    api_scope = "scope_knowledgebase"
