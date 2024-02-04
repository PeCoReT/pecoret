from backend.models.advisory_comment import AdvisoryComment
from backend.models.advisory_membership import Roles
from advisories.serializers.comment import AdvisoryCommentSerializer
from pecoret.core.viewsets import PeCoReTNoDestroyViewSet
from pecoret.core import permissions


class AdvisoryCommentViewSet(PeCoReTNoDestroyViewSet):
    """manage advisory comments"""

    queryset = AdvisoryComment.objects.none()
    api_scope = "scope_advisories"
    permission_classes = [
        permissions.AdvisoryPermission(
            read_write_roles=[Roles.CREATOR, Roles.VENDOR],
            read_only_roles=[Roles.READ_ONLY],
        )
    ]
    serializer_class = AdvisoryCommentSerializer

    def get_queryset(self):
        qs = AdvisoryComment.objects.for_advisory(self.request.advisory)
        if self.action in ["list", "retrieve"]:
            return qs
        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(advisory=self.request.advisory, user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user_edit=self.request.user)
