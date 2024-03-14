import datetime
import collections
from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from asmonitor.models import Program, Finding
from asmonitor.serializers.program import ProgramSerializer
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet


class ProgramViewSet(PeCoReTModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[
                permissions.Groups.GROUP_PENTESTER
            ],
            read_only_groups=[]
        )
    ]
    api_scope = 'scope_asmonitor'
    search_fields = ['name', 'description']

    @action(methods=['get'], detail=True)
    def stats_findings_by_date(self, request, *args, **kwargs):
        program = self.get_object()
        findings = Finding.objects.for_program(program).values('date_created__date').annotate(
            count=Count('pk')).order_by('-date_created__date')[:5]
        data = {}
        dates = findings.values_list('date_created__date', flat=True)
        for i in range(0, 5):
            last_day = (datetime.datetime.now() - datetime.timedelta(days=i)).date()
            if last_day not in dates:
                data[str(last_day)] = 0
            else:
                for finding in findings:
                    if last_day == finding['date_created__date']:
                        data[str(last_day)] = finding['count']
                        break
        data = collections.OrderedDict(sorted(data.items()))
        return Response(data, status=status.HTTP_200_OK)
