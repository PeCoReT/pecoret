from backend.api.serializers.reports import ReportSerializer
from backend.models.reports.report import Report
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core.utils.schema import extend_viewset_schema


@extend_viewset_schema(tags=['Reporting'], verbose_name='report')
class ProjectReportViewSet(PeCoReTModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.none()
    filterset_class = None
    search_fields = ["name"]
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]
    api_scope = "scope_all_projects"

    def get_queryset(self):
        return Report.objects.for_project(self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project)
