from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.permissions import IsAuthenticated
from backend.serializers.user_settings import UserSettingsSerializer
from backend.models import UserSettings
from pecoret.core.viewsets import PeCoReTListUpdateRetrieveModelViewSet


@extend_schema_view(
    list=extend_schema(operation_id='Get all user settings', tags=['Users']),
    retrieve=extend_schema(operation_id='Get a specific user setting', tags=['Users']),
    partial_update=extend_schema(operation_id='Partially update a user setting', tags=['Users']),
)
class UserSettingsViewSet(PeCoReTListUpdateRetrieveModelViewSet):
    serializer_class = UserSettingsSerializer
    queryset = UserSettings.objects.none()
    permission_classes = [IsAuthenticated]
    api_scope = "scope_user"

    def get_object(self):
        return UserSettings.objects.for_user(self.request.user).get()
