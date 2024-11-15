from drf_spectacular.utils import extend_schema_view, extend_schema
from extra_settings.models import Setting
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.api.serializers.settings import SettingSerializer
from pecoret.core import permissions
from pecoret.core.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin
from pecoret.core.viewsets import GenericViewSet


@extend_schema_view(
    advisories=extend_schema(operation_id='Get advisory settings', tags=['Settings']),
    list=extend_schema(operation_id='Get all settings', tags=['Settings']),
    retrieve=extend_schema(operation_id='Get a specific setting', tags=['Settings']),
    update=extend_schema(operation_id='Update a specific setting', tags=['Settings']),
    general=extend_schema(operation_id='Get all general settings', tags=['Settings']),
    partial_update=extend_schema(operation_id='Partially update a setting', tags=['Settings']),
)
class SettingViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Setting.objects.all()
    api_scope = None
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[],
            read_only_groups=[]
        )
    ]
    serializer_class = SettingSerializer

    @action(detail=False, methods=['get'], serializer_class=SettingSerializer)
    def general(self, request, *args, **kwargs):
        qs = self.get_queryset().filter(name__startswith='GENERAL_')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], serializer_class=SettingSerializer)
    def advisories(self, *args, **kwargs):
        qs = self.get_queryset().filter(name__startswith='ADVISORY_')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
