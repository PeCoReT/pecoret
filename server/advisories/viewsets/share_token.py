from advisories.models.share_token import ShareToken
from advisories.serializers.share_token import ShareTokenSerializer
from pecoret.core import mixins
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_schema, extend_schema_view
from pecoret.core.viewsets import GenericViewSet


@extend_schema_view(
    retrieve=extend_schema(operation_id='Get a specific share token', tags=['Advisories']),
    list=extend_schema(operation_id='List share tokens', tags=['Advisories']),
    delete=extend_schema(operation_id='Delete a share token', tags=['Advisories']),
    create=extend_schema(operation_id='Create a new share token', tags=['Advisories']),
)
class ShareTokenViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin,
                        mixins.DestroyModelMixin, GenericViewSet):
    queryset = ShareToken.objects.none()
    api_scope = 'scope_advisories'
    search_fields = ['name']
    ordering_fields = ["date_expire"]
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[permissions.Groups.GROUP_PENTESTER],
            read_only_groups=[]
        )
    ]
    serializer_class = ShareTokenSerializer

    def get_queryset(self):
        return ShareToken.objects.for_advisory(self.kwargs.get('advisory'))

    def perform_create(self, serializer):
        serializer.save(advisory_id=self.kwargs.get('advisory'))
