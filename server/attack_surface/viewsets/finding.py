from django.conf import settings
from django.http import HttpResponse
from rest_framework.decorators import action

from attack_surface.serializers.finding import FindingSerializer
from attack_surface.models.finding import Finding
from attack_surface.tasks import export_finding_pdf
from pecoret.core import permissions
from pecoret.core.permissions.locked_item import LockedItemPermission
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core.mixins.locked_model import LockedItemMixin


@extend_viewset_schema(tags=["Attack Surface"], verbose_name="finding")
class FindingViewSet(LockedItemMixin, PeCoReTModelViewSet):
    queryset = Finding.objects.all()
    api_scope = "scope_attack_surface"
    serializer_class = FindingSerializer
    ordering_fields = ["date_created", "date_updated", "severity"]
    search_fields = ["title"]
    permission_classes = [
        LockedItemPermission,
        permissions.GroupPermission(
            read_only_groups=[], read_write_groups=[permissions.Groups.GROUP_PENTESTER]
        ),
    ]

    def perform_create(self, serializer):
        serializer.save(created_by_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by_user=self.request.user)

    @action(detail=True, methods=["get"])
    def export_pdf(self, request, **kwargs):
        """export the advisory details as PDF attachment

        Returns:
            HttpResponse: PDF Response
        """
        finding = self.get_object()
        if settings.AS_REPORT_TEMPLATE:
            report_template = settings.AS_REPORT_TEMPLATE
        else:
            report_template = list(settings.REPORT_TEMPLATES.keys())[0]
        result = export_finding_pdf(finding, report_template)
        response = HttpResponse(result, content_type="application/pdf")
        filename = f"finding-{finding.finding_id}"
        response["Content-Disposition"] = f"attachment; filename={filename}.pdf"
        return response
