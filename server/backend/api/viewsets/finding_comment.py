from drf_spectacular.utils import extend_schema, extend_schema_view
from backend.api.serializers.finding_comment import FindingCommentSerializer
from backend.models import FindingComment
from pecoret.core.viewsets import PeCoReTNoDestroyViewSet
from pecoret.core import permissions


@extend_schema_view(
    list=extend_schema(operation_id='Get all finding comments', tags=['Findings']),
    retrieve=extend_schema(operation_id='Get specific finding comment', tags=['Findings']),
    update=extend_schema(operation_id='Update specific finding comment', tags=['Findings']),
    partial_update=extend_schema(operation_id='Partially update specific finding comment', tags=['Findings']),
    create=extend_schema(operation_id='Create a new finding comment', tags=['Findings']),
)
class FindingCommentViewSet(PeCoReTNoDestroyViewSet):
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY, permissions.FindingPermission]
    queryset = FindingComment.objects.none()
    serializer_class = FindingCommentSerializer
    api_scope = "scope_all_projects"

    def get_queryset(self):
        return FindingComment.objects.for_project(self.request.project).for_finding(
            self.request.finding
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, finding=self.request.finding)

    def perform_update(self, serializer):
        serializer.save(user_edit=self.request.user)
