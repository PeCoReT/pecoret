from django.http import HttpResponse
from django.utils.text import slugify
from django_q.tasks import async_task
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.models.reports.report_release import ReportRelease, ReleaseType
from backend.api.serializers.reports.release import ReportReleaseSerializer
from backend.tasks.reporting import create_report_document_task
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTNoUpdateViewSet


@extend_schema_view(
    list=extend_schema(operation_id='Get all report documents/releases', tags=['Reporting']),
    destroy=extend_schema(operation_id='Delete a report document/release', tags=['Reporting']),
    retrieve=extend_schema(operation_id='Get a specific report document/release', tags=['Reporting']),
    create=extend_schema(operation_id='Create a new report document/release', tags=['Reporting']),
    download=extend_schema(operation_id='Download a report document/release', tags=['Reporting']),
    preview_document=extend_schema(operation_id='Get the preview report release', tags=['Reporting'])
)
class ReportReleaseViewSet(PeCoReTNoUpdateViewSet):
    serializer_class = ReportReleaseSerializer
    queryset = ReportRelease.objects.none()
    filterset_class = None
    search_fields = []
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY, permissions.ReportPermission]
    api_scope = "scope_all_projects"

    def get_queryset(self):
        qs = ReportRelease.objects.for_project(self.request.project).for_report(self.request.report)
        if self.action == "list":
            # exclude Preview documents from list view
            qs = qs.exclude(release_type=ReleaseType.PREVIEW)
        return qs

    def perform_create(self, serializer):
        instance = serializer.save(report=self.request.report)
        task_id = async_task(create_report_document_task, instance.pk)
        instance.task_id = task_id
        instance.save()

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None, project=None, report=None):
        document = self.get_object()
        response = HttpResponse(
            document.compiled_source, content_type=document.content_type
        )
        if document.release_type == ReleaseType.PREVIEW:
            release_type = 'preview'
        elif document.release_type == ReleaseType.DRAFT:
            release_type = f'{document.report.get_current_version()}-draft'
        else:
            release_type = document.report.get_current_version()
        filename = (f'{self.request.project.company.name}-{self.request.project.name}-'
                    f'{self.request.project.year}-{release_type}.{document.file_extension}')
        filename = slugify(filename)
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response

    @action(detail=False, methods=["get"])
    def preview_document(self, *args, **kwargs):
        """
        get the `ReleaseType.PREVIEW` document details
        :param args:
        :param kwargs:
        :return:
        """
        obj = self.request.report
        qs = ReportRelease.objects.for_project(self.request.project).for_report(obj).preview()
        if qs.exists():
            serializer = self.get_serializer(qs.get())
            data = serializer.data
        else:
            data = {}
        return Response(data)
