from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from attack_surface.filters.scan_finding import ScanFindingFilter
from attack_surface.mixins import ScanningAuthMixin
from attack_surface.models.scan_finding import ScanFinding, ScanFindingStatus
from attack_surface.permissions import ScanningPermission
from attack_surface.serializers.scan_finding import ScanFindingSerializer, ScanFindingStatusUpdateSerializer
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet


@extend_viewset_schema(tags=['Attack Surface'], verbose_name='scan finding')
@extend_schema_view(
    create_or_update=extend_schema(operation_id='Get or create a scan finding', tags=['Attack Surface'])
)
class ScanFindingViewSet(ScanningAuthMixin, PeCoReTModelViewSet):
    queryset = ScanFinding.objects.all()
    serializer_class = ScanFindingSerializer
    permission_classes = [
        ScanningPermission(read_write_groups=[], read_only_groups=[permissions.Groups.GROUP_PENTESTER],
                           scanner_write=True, scanner_read=True)
    ]
    api_scope = 'scope_attack_surface'
    search_fields = ['name', 'affected_component']
    ordering_field = ['date_created', 'date_updated', 'severity']
    filterset_class = ScanFindingFilter

    def get_permissions(self):
        if self.action == 'partial_update':
            # allow pentesters to change status and comment
            return [
                ScanningPermission(read_write_groups=[permissions.Groups.GROUP_PENTESTER],
                           scanner_write=True, scanner_read=True)
            ]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'partial_update':
            # allow pentesters to change status and comment
            return ScanFindingStatusUpdateSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["post"])
    def create_or_update(self, request, *args, **kwargs):
        qs = ScanFinding.objects.filter_unique(request.data['name'],
                                               request.data['affected_component'],
                                               request.data['severity'])
        if qs.exists():
            instance = qs.get()
            # if a finding exists, ensure it is re-opened
            request.data['status'] = ScanFindingStatus.OPEN.label
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            # if instance should be ignored until specific date, skip
            if instance.ignore_until and timezone.now().date() <= instance.ignore_until:
                return Response(serializer.data, status=status.HTTP_200_OK)
            self.perform_update(serializer)
            return Response(serializer.data, status.HTTP_200_OK)
        # create
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
