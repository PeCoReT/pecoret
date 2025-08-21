from attack_surface.filters.finding_component import FindingComponentFilter
from attack_surface.models import FindingComponent
from attack_surface.serializers.finding_component import FindingComponentSerializer
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions


@extend_viewset_schema(tags=["Attack Surface"], verbose_name="Finding Component")
class FindingComponentViewSet(PeCoReTModelViewSet):
    queryset = FindingComponent.objects.all()
    serializer_class = FindingComponentSerializer
    api_scope = "scope_attack_surface"
    search_fields = ["data"]
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[permissions.Groups.GROUP_PENTESTER], read_only_groups=[]
        )
    ]
    filterset_class = FindingComponentFilter
