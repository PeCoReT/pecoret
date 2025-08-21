from pecoret.core.viewsets import ModelViewSet
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema
from advisories.models.label import Label
from advisories.serializers.label import LabelSerializer


@extend_viewset_schema(tags=['Advisories'], verbose_name='label')
class LabelViewSet(ModelViewSet):
    permission_classes = [permissions.GroupPermission(
        read_write_groups=[permissions.Groups.GROUP_PENTESTER],
        read_only_groups=[]
    )]
    filterset_class = None
    search_fields = ["name", "description"]
    ordering_fields = []
    serializer_class = LabelSerializer
    api_scope = 'scope_advisories'

    def get_queryset(self):
        return Label.objects.all()
