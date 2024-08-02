from django.conf import settings
from django.db.models import Count
from django.http.response import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response

from advisories.filters import AdvisoryFilter
from advisories.models.advisory import Advisory
from advisories.serializers.advisory import (
    AdvisorySerializer,
    AdvisoryCreateSerializer,
    AdvisoryUpdateSerializer,
    AdvisoryDownloadSerializer
)
from backend.tasks.reporting import export_advisory
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema, extend_schema, extend_schema_view
from pecoret.core.viewsets import PeCoReTModelViewSet


@extend_viewset_schema(tags=['Advisories'], verbose_name='advisory')
@extend_schema_view(
    preview=extend_schema(tags=['Advisories'], operation_id='Preview Advisory PDF'),
    export_pdf=extend_schema(tags=['Advisories'], operation_id='Export Advisory PDF'),
    top_submitters=extend_schema(operation_id='Get top submitters', tags=['Advisory Statistics']),
    top_vulnerabilities=extend_schema(operation_id='Get top vulnerabilities statistics', tags=['Advisory Statistics']),
    top_vendors=extend_schema(operation_id='Get top vendors statistics', tags=['Advisory Statistics']),
    top_products=extend_schema(operation_id='Get top products statistics', tags=['Advisory Statistics']),
    statistics_base_information=extend_schema(operation_id='Get base statistic information',
                                              tags=['Advisory Statistics']),
)
class AdvisoryViewSet(PeCoReTModelViewSet):
    queryset = Advisory.objects.none()
    filterset_class = AdvisoryFilter
    api_scope = "scope_advisories"
    search_fields = ["vulnerability__vulnerability_id", "product", "vendor_name", "internal_name"]
    ordering_fields = ["advisory_id", "date_planned_disclosure", "date_created", "date_updated"]
    serializer_class = AdvisorySerializer
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[permissions.Groups.GROUP_PENTESTER], read_only_groups=[]
        )]

    def get_queryset(self):
        return Advisory.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return AdvisoryCreateSerializer
        if self.action in ["list", "retrieve"]:
            return AdvisorySerializer
        return AdvisoryUpdateSerializer

    @action(detail=True, methods=["get"], serializer_class=AdvisoryDownloadSerializer)
    def export_pdf(self, request, **kwargs):
        """export the advisory details as PDF attachment

        Returns:
            HttpResponse: PDF Response
        """
        advisory = self.get_object()
        if not advisory.report_template:
            advisory.report_template = list(settings.REPORT_TEMPLATES.keys())[0]
        result = export_advisory(advisory, advisory.report_template)
        response = HttpResponse(result, content_type="application/pdf")
        filename = f"advisory-{advisory.pk}"
        response["Content-Disposition"] = f"attachment; filename={filename}.pdf"
        return response

    @action(detail=True, methods=["get"])
    def preview(self, request, *args, **kwargs):
        advisory = self.get_object()
        result = export_advisory(advisory, advisory.report_template)
        response = HttpResponse(result, content_type="application/pdf")
        response["Content-Disposition"] = "inline"
        return response

    @action(detail=False, methods=["get"], url_path="statistics/top-submitters")
    def top_submitters(self, request, *args, **kwargs):
        """list top advisory submitters"""
        qs = self.get_queryset().count_by_user()
        return Response(list(qs)[:10])

    @action(detail=False, methods=["get"], url_path="statistics/top-vulnerabilities")
    def top_vulnerabilities(self, request, *args, **kwargs):
        qs = self.get_queryset().values("vulnerability__name").annotate(count=Count('pk')).order_by("-count")
        return Response(list(qs)[:10])

    @action(detail=False, methods=["get"], url_path="statistics/top-vendors")
    def top_vendors(self, request, *args, **kwargs):
        qs = self.get_queryset().filter(technology__vendor__isnull=False).values("technology__vendor").annotate(
            count=Count('pk')).order_by("-count")
        return Response(list(qs)[:10])

    @action(detail=False, methods=["get"], url_path="statistics/top-products")
    def top_products(self, request, *args, **kwargs):
        qs = self.get_queryset().values("technology__name", "technology__vendor").annotate(count=Count('pk')).order_by(
            "-count")
        return Response(list(qs)[:10])

    @action(detail=False, methods=["get"], url_path="statistics/base-information")
    def statistics_base_information(self, request, *args, **kwargs):
        qs = self.get_queryset()
        data = {
            "inbox_count": qs.count(),
            "inbox_unfixed_count": qs.unfixed().count(),
            "inbox_fixed_count": qs.fixed().count(),
            "inbox_wontfix_count": qs.wont_fix().count(),
            "inbox_next_disclosure_date": None
        }
        if qs.count() > 0:
            data["inbox_next_disclosure_date"] = qs.order_by("-date_planned_disclosure").first().date_planned_disclosure
        return Response(data)
