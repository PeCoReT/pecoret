from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from attack_surface.models.scan_finding import ScanFinding
from attack_surface.serializers.scan_finding import ScanFindingSerializer
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet


class ScanFindingViewSet(PeCoReTModelViewSet):
    queryset = ScanFinding.objects.all()
    serializer_class = ScanFindingSerializer
    permission_classes = [
        permissions.GroupPermission(
            read_only_groups=[],
            read_write_groups=[permissions.Groups.GROUP_PENTESTER]
        )
    ]
    api_scope = 'scope_attack_surface'
    search_fields = ['name', 'affected_component']
    ordering_field = ['date_created', 'date_updated', 'severity']
    filterset_class = None

    @action(detail=False, methods=["post"])
    def create_or_update(self, request, *args, **kwargs):
        qs = ScanFinding.objects.filter_unique(request.data['program'], request.data['name'],
                                               request.data['affected_component'],
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
