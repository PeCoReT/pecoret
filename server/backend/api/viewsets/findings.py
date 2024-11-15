from django.http.response import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from backend.models import Finding, FindingTimeline
from backend.api.serializers.finding import (
    FindingSerializer,
    FindingCreateSerializer,
    FindingCopySerializer,
    FindingAsAdvisorySerializer,
)
from backend.api.filters.finding import FindingFilter
from backend.tasks.reporting import export_single_finding
from advisories.models.advisory import Advisory
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema


@extend_viewset_schema(tags=['Findings'], verbose_name='finding')
@extend_schema_view(
    export_pdf=extend_schema(tags=['Findings'], operation_id='Export PDF'),
    preview=extend_schema(tags=['Findings'], operation_id='Preview PDF'),
    as_advisory=extend_schema(tags=['Findings'], operation_id='Advisory from Finding'),
    copy=extend_schema(tags=['Findings'], operation_id='Copy Finding'),
)
class FindingViewSet(PeCoReTModelViewSet):
    queryset = Finding.objects.none()
    filterset_class = FindingFilter
    search_fields = [
        "name",
        "vulnerability__vulnerability_id",
        "vulnerability__name",
        "needs_review",
    ]
    api_scope = "scope_all_projects"
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]

    def get_queryset(self):
        return Finding.objects.for_project(self.request.project)

    def get_serializer_class(self):
        if self.action == "create":
            return FindingCreateSerializer
        return FindingSerializer

    @action(detail=True, methods=["get"])
    def export_pdf(self, request, *args, **kwargs):
        finding = self.get_object()
        # export finding using company-wide report_template
        template = request.project.company.report_template
        result = export_single_finding(finding, template)
        response = HttpResponse(result, content_type="application/pdf")
        filename = "finding_%s.pdf" % finding.unique_id.lower()
        response["Content-Disposition"] = "attachment; filename=%s" % filename
        return response

    @action(detail=True, methods=["get"])
    def preview(self, request, *args, **kwargs):
        finding = self.get_object()
        # export finding using company-wide report_template
        template = request.project.company.report_template
        result = export_single_finding(finding, template)
        response = HttpResponse(result, content_type="application/pdf")
        response["Content-Disposition"] = "inline"
        return response

    @action(detail=True, methods=["post"], serializer_class=FindingCopySerializer)
    def copy(self, request, project=None, pk=None):
        obj = self.get_object()
        new_finding = Finding.objects.copy_from_finding(obj)
        serializer = FindingCopySerializer(new_finding, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, project=self.request.project)

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.old_status != instance.status:
            title = "changed status to %s" % instance.get_status_display()
            FindingTimeline.objects.create(
                user=self.request.user, title=title, text="", finding=instance
            )

    @action(
        detail=True,
        methods=["post"],
        serializer_class=FindingAsAdvisorySerializer,
    )
    def as_advisory(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = FindingAsAdvisorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Advisory.objects.create_from_finding(obj, **serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
