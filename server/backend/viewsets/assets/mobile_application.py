from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from backend.models.assets.mobile_application import MobileApplication
from backend.serializers.assets.mobile_application import MobileApplicationSerializer


@extend_viewset_schema(tags=['Projects'], verbose_name='mobile application asset')
class MobileApplicationViewSet(PeCoReTModelViewSet):
    permission_classes = [
        permissions.PRESET_PENTESTER_OR_READONLY
    ]
    api_scope = "scope_all_projects"
    queryset = MobileApplication.objects.none()
    serializer_class = MobileApplicationSerializer
    filterset_class = None
    search_fields = ["name"]
    ordering_fields = ["name", "date_created", "date_updated"]

    def get_queryset(self):
        return MobileApplication.objects.for_project(self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project)
