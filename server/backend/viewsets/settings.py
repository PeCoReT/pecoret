from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from pecoret.core.viewsets import GenericViewSet
from pecoret.core import permissions
from backend.serializers.settings import SettingSerializer
from backend.models.settings import Settings


class SettingViewSet(GenericViewSet):
    queryset = Settings.objects.all()
    api_scope = None
    permission_classes = [
        permissions.GroupPermission(
            read_write_groups=[], read_only_groups=[]
        )
    ]
    serializer_class = SettingSerializer

    def get_object(self):
        return Settings.objects.first()

    @action(detail=False, methods=['patch', 'get'], serializer_class=SettingSerializer)
    def general(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.method.lower() == 'get':
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = SettingSerializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
