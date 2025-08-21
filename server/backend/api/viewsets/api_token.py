from drf_spectacular.utils import extend_schema_view, extend_schema
from backend.api.serializers.api_token import APITokenSerializer
from backend.models import APIToken
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTNoUpdateViewSet


@extend_schema_view(
    list=extend_schema(
        operation_id='Get all API tokens', tags=['API Tokens']
    ),
    retrieve=extend_schema(
        operation_id='Get a specific API token', tags=['API Tokens']
    ),
    destroy=extend_schema(
        operation_id='Delete a API token', tags=['API Tokens']
    ),
    create=extend_schema(
        operation_id='Create a new API token', tags=['API Tokens']
    )
)
class APITokenViewSet(PeCoReTNoUpdateViewSet):
    queryset = APIToken.objects.none()
    search_fields = ["name"]
    ordering_fields = ['date_created', 'date_updated']
    serializer_class = APITokenSerializer
    api_scope = None  # do not allow api tokens to configure api tokens
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[
                permissions.Groups.GROUP_MANAGEMENT,
                permissions.Groups.GROUP_PENTESTER,
            ],
            read_only_groups=[]
        )
    ]

    def get_queryset(self):
        return APIToken.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
