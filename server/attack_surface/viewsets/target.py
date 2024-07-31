from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from attack_surface.serializers.target import TargetSerializer, Target
from attack_surface.filters.target import TargetFilter


@extend_viewset_schema(tags=['Attack Surface'], verbose_name='target')
@extend_schema_view(
    create_or_update=extend_schema(operation_id='Get or create a target', tags=['Attack Surface'])
)
class TargetViewSet(PeCoReTModelViewSet):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[permissions.Groups.GROUP_PENTESTER],
            read_only_groups=[]
        )
    ]
    api_scope = 'scope_attack_surface'
    search_fields = ['data']
    ordering_fields = ['date_created', 'date_updated', 'first_seen', 'last_seen']
    filterset_class = TargetFilter

    @action(detail=False, methods=["post"])
    def create_or_update(self, request, *args, **kwargs):
        qs = Target.objects.filter(data=request.data.get('data'), program__pk=request.data.get('program'))
        if qs.exists():
            serializer = self.get_serializer(qs.get(), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status.HTTP_200_OK)
        # create
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
