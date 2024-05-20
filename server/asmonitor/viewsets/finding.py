from django.http.response import HttpResponse
from rest_framework.decorators import action
from asmonitor.models import Finding
from asmonitor.permissions import ASMonitorGroupPermission
from asmonitor.filters.finding import FindingFilter
from asmonitor.serializers.finding import FindingSerializer, GlobalFindingSerializer
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet, GenericViewSet
from pecoret.core.mixins import ListModelMixin


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

    """
    @action(detail=True, method=['get'])
    def export_pdf(self, request, *args, **kwargs):
        finding = self.get_object()
        template = request.GET.get('template', 'default_template')
        result = export_finding(finding, template)
        response = HttpResponse(result, content_type='application/pdf')
        response['Content-Disposition'] = 'inline'
        return response
    """


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
