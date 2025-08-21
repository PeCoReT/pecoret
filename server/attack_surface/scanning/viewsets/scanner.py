from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response

from attack_surface.authentication import ScannerAuth
from attack_surface.mixins import ScanFeatureDispatchMixin, ScanningAuthMixin
from attack_surface.models.scanner import Scanner
from attack_surface.permissions import ScanningPermission
from attack_surface.scanning.serializers.scanner import ScannerSerializer, ScannerCreateSerializer
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet


@extend_viewset_schema(['Attack Surface Scanning'], verbose_name='scanner')
class ScannerViewSet(ScanFeatureDispatchMixin, ScanningAuthMixin, PeCoReTModelViewSet):
    queryset = Scanner.objects.all()
    serializer_class = ScannerSerializer
    permission_classes = []
    api_scope = 'scope_attack_surface'
    search_fields = ['name']
    ordering_fields = ['last_seen', 'date_created', 'date_updated']

    def get_permissions(self):
        if self.action == 'create':
            # only allow admin to create
            return [permissions.GroupPermission(read_write_groups=[], read_only_groups=[])]
        elif self.action == 'ping':
            return [ScanningPermission(scanner_read=True, scanner_write=True)]
        return [
            permissions.GroupPermission(read_write_groups=[], read_only_groups=[permissions.Groups.GROUP_PENTESTER])]

    def get_serializer_class(self):
        if self.action == 'create':
            return ScannerCreateSerializer
        return self.serializer_class

    @action(detail=False, methods=['post'], authentication_classes=[ScannerAuth],
            permission_classes=[ScanningPermission(scanner_read=True, scanner_write=True)])
    def ping(self, request, *args, **kwargs):
        """ used by the scanner to set alive status """
        scanner = request.scanner
        now = timezone.now()
        scanner.last_seen = now
        scanner.save()
        serializer = ScannerSerializer(scanner)
        return Response(serializer.data)
