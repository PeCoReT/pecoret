from advisories.models.advisory_timeline import AdvisoryTimeline
from advisories.models.advisory_membership import Roles
from advisories.serializers.timeline import AdvisoryTimelineSerializer
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema


@extend_viewset_schema(tags=['Advisories'], verbose_name='timeline')
class AdvisoryTimelineViewSet(PeCoReTModelViewSet):
    queryset = AdvisoryTimeline.objects.none()
    api_scope = "scope_advisories"
    permission_classes = [
        permissions.AdvisoryPermission(
            read_write_roles=[Roles.CREATOR],
            read_only_roles=[Roles.READ_ONLY, Roles.VENDOR],
        )
    ]
    serializer_class = AdvisoryTimelineSerializer

    def get_queryset(self):
        return AdvisoryTimeline.objects.for_advisory(self.request.advisory)

    def perform_create(self, serializer):
        serializer.save(advisory=self.request.advisory)
