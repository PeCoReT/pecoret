from pecoret.core.viewsets import ModelViewSet
from pecoret.core import permissions
from advisories.models.label import Label
from advisories.serializers.label import LabelSerializer


class LabelViewSet(ModelViewSet):
    permission_classes = [permissions.GroupPermission(
        read_write_groups=[permissions.Groups.ADVISORY_MANAGEMENT],
        read_only_groups=[permissions.Groups.ADVISORY_MANAGEMENT, permissions.Groups.GROUP_PENTESTER]
    )]
    filterset_class = None
    search_fields = ["name", "description"]
    ordering_fields = []
    serializer_class = LabelSerializer

    def get_queryset(self):
        return Label.objects.all()
