from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from backend.models.assets.service import Service
from backend.serializers.assets.service import ServiceSerializer
from backend.filters.service import ServiceFilter


@extend_viewset_schema(tags=['Projects'], verbose_name='service asset')
class ServiceViewSet(PeCoReTModelViewSet):
    permission_classes = [
        permissions.PRESET_PENTESTER_OR_READONLY
    ]
    api_scope = "scope_all_projects"
    queryset = Service.objects.none()
    serializer_class = ServiceSerializer
    filterset_class = ServiceFilter
    search_fields = ["port", "name", "product", "host__ip", "host__dns"]
    ordering_fields = ["port", "name", "host__ip", "host__dns", "date_created", "date_updated"]

    def get_queryset(self):
        return Service.objects.for_project(self.request.project)
