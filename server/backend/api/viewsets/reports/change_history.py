from backend.api.serializers.reports.change_history import ChangeHistorySerializer
from backend.models.reports.change_history import ChangeHistory
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core.utils.schema import extend_viewset_schema


@extend_viewset_schema(tags=['Reporting'], verbose_name='change history')
class ChangeHistoryViewSet(PeCoReTModelViewSet):
    serializer_class = ChangeHistorySerializer
    queryset = ChangeHistory.objects.none()
    filterset_class = None
    search_fields = []
    api_scope = "scope_all_projects"
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY, permissions.ReportPermission]

    def get_queryset(self):
        return ChangeHistory.objects.for_project(self.request.project).filter(
            report=self.request.report
        )

    def perform_create(self, serializer):
        serializer.save(report=self.request.report)
