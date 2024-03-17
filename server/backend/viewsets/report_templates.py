from backend.models import ReportTemplate
from backend.serializers.report_templates import ReportTemplateSerializer, ReportTemplateMinimalSerializer
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet


class ReportTemplateViewSet(PeCoReTModelViewSet):
    serializer_class = ReportTemplateSerializer
    queryset = ReportTemplate.objects.none()
    search_fields = ["name"]
    api_scope = None
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[
                permissions.Groups.SUPERUSER
            ],
            read_only_groups=[
                permissions.Groups.GROUP_MANAGEMENT,
                permissions.Groups.GROUP_PENTESTER
            ]
        )
    ]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ReportTemplate.objects.all()
        return ReportTemplate.objects.active()

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return ReportTemplateSerializer
        return ReportTemplateMinimalSerializer
