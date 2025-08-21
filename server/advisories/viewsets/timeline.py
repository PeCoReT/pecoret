from advisories.models.advisory_timeline import AdvisoryTimeline
from advisories.serializers.timeline import AdvisoryTimelineSerializer
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema


@extend_viewset_schema(tags=['Advisories'], verbose_name='timeline')
class AdvisoryTimelineViewSet(PeCoReTModelViewSet):
    queryset = AdvisoryTimeline.objects.none()
    api_scope = "scope_advisories"
    permission_classes = [
        permissions.GroupPermission(
            read_only_groups=[],
            read_write_groups=[permissions.Groups.GROUP_PENTESTER],
        )
    ]
    serializer_class = AdvisoryTimelineSerializer

    def get_queryset(self):
        return AdvisoryTimeline.objects.for_advisory(self.kwargs.get('advisory'))

    def perform_create(self, serializer):
        serializer.save(advisory_id=self.kwargs.get('advisory'))
