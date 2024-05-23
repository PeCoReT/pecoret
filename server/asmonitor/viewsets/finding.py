from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from asmonitor.filters.finding import FindingFilter
from asmonitor.models import Finding
from asmonitor.permissions import ASMonitorGroupPermission
from asmonitor.serializers.finding import FindingSerializer, GlobalFindingSerializer
from pecoret.core import permissions
from pecoret.core.mixins import ListModelMixin
from pecoret.core.viewsets import PeCoReTModelViewSet, GenericViewSet


class FindingViewSet(PeCoReTModelViewSet):
    queryset = Finding.objects.none()
    serializer_class = FindingSerializer
    search_fields = ['name']
    ordering_fields = ['severity', 'date_updated', 'date_created']
    filterset_class = FindingFilter
    api_scope = 'scope_asmonitor'
    permission_classes = [
        ASMonitorGroupPermission(
            read_write_groups=[
                permissions.Groups.GROUP_PENTESTER
            ],
            read_only_groups=[]
        )
    ]

    def get_queryset(self):
        return Finding.objects.for_program(program=self.request.program)

    def perform_create(self, serializer):
        serializer.save(program=self.request.program, user=self.request.user)

    @action(detail=False, methods=["post"])
    def create_or_update(self, request, *args, **kwargs):
        serializer = FindingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        qs = Finding.objects.filter_unique(request.program, request.data['name'], request.data['target'],
                                           request.data['severity'])
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


class GlobalFindingList(ListModelMixin, GenericViewSet):
    queryset = Finding.objects.all()
    serializer_class = GlobalFindingSerializer
    filterset_class = FindingFilter
    search_fields = ['name']
    ordering_fields = ['severity', 'date_updated', 'date_created']
    api_scope = 'scope_asmonitor'
    permission_classes = [
        ASMonitorGroupPermission(
            read_write_groups=[
                permissions.Groups.GROUP_PENTESTER
            ],
            read_only_groups=[]
        )
    ]
