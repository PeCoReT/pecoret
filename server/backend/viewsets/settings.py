from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from extra_settings.models import Setting
from pecoret.core.viewsets import GenericViewSet
from pecoret.core.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin
from pecoret.core import permissions
from backend.serializers.settings import SettingSerializer


class SettingViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = Setting.objects.all()
    api_scope = None
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[], read_only_groups=[]
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
