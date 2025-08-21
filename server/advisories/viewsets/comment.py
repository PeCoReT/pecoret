from drf_spectacular.utils import extend_schema, extend_schema_view
from advisories.models.advisory_comment import AdvisoryComment
from advisories.serializers.comment import AdvisoryCommentSerializer
from pecoret.core.viewsets import PeCoReTNoDestroyViewSet
from pecoret.core import permissions


@extend_schema_view(
    list=extend_schema(operation_id='Get all advisory comments', tags=['Advisories']),
    retrieve=extend_schema(operation_id='Get a specific advisory comment', tags=['Advisories']),
    create=extend_schema(operation_id='Create a new advisory comment', tags=['Advisories']),
    update=extend_schema(operation_id='Update a advisory comment', tags=['Advisories']),
    partial_update=extend_schema(operation_id='Partially update a advisory comment', tags=['Advisories']),
)
class AdvisoryCommentViewSet(PeCoReTNoDestroyViewSet):
    queryset = AdvisoryComment.objects.none()
    api_scope = "scope_advisories"
    permission_classes = [
        permissions.GroupPermission(
            read_only_groups=[],
            read_write_groups=[permissions.Groups.GROUP_PENTESTER],
        )
    ]
    serializer_class = AdvisoryCommentSerializer

    def get_queryset(self):
        qs = AdvisoryComment.objects.for_advisory(self.kwargs.get('advisory'))
        if self.action in ["list", "retrieve"]:
            return qs
        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(advisory_id=self.kwargs.get('advisory'), user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user_edit=self.request.user)
