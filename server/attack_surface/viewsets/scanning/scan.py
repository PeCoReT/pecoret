from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from attack_surface.authentication import ScannerAuth
from attack_surface.mixins import ScanFeatureDispatchMixin, ScanningAuthMixin
from attack_surface.models import Scan
from attack_surface.permissions import ScanningPermission
from attack_surface.serializers.scanning.scan import ScanSerializer, ScanUpdateSerializer, ScannerScanUpdateSerializer
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet


@extend_viewset_schema(tags=['Attack Surface Scanning'], verbose_name='scan')
class ScanViewSet(ScanFeatureDispatchMixin, ScanningAuthMixin, PeCoReTModelViewSet):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer
    permission_classes = [
        ScanningPermission(read_write_groups=[permissions.Groups.GROUP_PENTESTER], scanner_write=True,
                           scanner_read=True)]
    search_fields = ['scan_id', 'name', 'scan_type__name']
    api_scope = 'scope_attack_surface'

    def get_serializer_class(self):
        if self.action in ['partial_update', 'update'] and self.request.headers.get('X-Scanner-Auth'):
            return ScannerScanUpdateSerializer
        elif self.action in ['partial_update', 'update']:
            return ScanUpdateSerializer
        return self.serializer_class

    @action(methods=['get'], detail=False,
            permission_classes=[ScanningPermission(scanner_read=True, scanner_write=True)], authentication_classes=[
            ScannerAuth])
    def fetch_next_scan(self, request, *args, **kwargs):
        # TODO: let scanner submit their queue names so they receive only tasks they can do
        with transaction.atomic():
            scan = Scan.objects.select_for_update(skip_locked=True).pending().order_by('date_created').first()
            if not scan:
                return Response([], status=status.HTTP_200_OK)
            serializer = self.get_serializer(scan)
            scan.start_scan()
            return Response(serializer.data, status=status.HTTP_200_OK)
