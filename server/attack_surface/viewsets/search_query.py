from attack_surface.models import UserSearchQuery
from attack_surface.serializers.search_query import UserSearchQuerySerializer
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions


class UserSearchQueryViewSet(PeCoReTModelViewSet):
    serializer_class = UserSearchQuerySerializer
    search_fields = ['name']
    api_scope = 'scope_attack_surface'
    ordering_fields = ['date_created', 'date_updated', 'name']
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[permissions.Groups.GROUP_PENTESTER],
            read_only_groups=[]
        )
    ]

    def get_queryset(self):
        return UserSearchQuery.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
