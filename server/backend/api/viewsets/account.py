from backend.models import Account
from backend.api.serializers.account import AccountSerializer
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema


@extend_viewset_schema(tags=['Accounts'], verbose_name='account')
class AccountViewSet(PeCoReTModelViewSet):
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]
    queryset = Account.objects.none()
    filterset_class = None
    search_fields = ["username"]
    serializer_class = AccountSerializer
    api_scope = "scope_all_projects"

    def get_queryset(self):
        return Account.objects.for_project(self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project)
