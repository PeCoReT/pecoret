from backend.serializers.api_token import APITokenSerializer
from backend.models import APIToken
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTNoUpdateViewSet


class APITokenViewSet(PeCoReTNoUpdateViewSet):
    queryset = APIToken.objects.none()
    search_fields = ["name"]
    serializer_class = APITokenSerializer
    api_scope = None  # do not allow api tokens to configure api tokens
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[
                permissions.Groups.GROUP_MANAGEMENT,
                permissions.Groups.GROUP_PENTESTER,
                permissions.Groups.ADVISORY_MANAGEMENT
            ],
            read_only_groups=[]
        )
    ]

    def get_queryset(self):
        return APIToken.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
