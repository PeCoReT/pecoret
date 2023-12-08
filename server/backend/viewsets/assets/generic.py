from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core import permissions
from backend.serializers.assets.generic import GenericAssetSerializer
from backend.models import GenericAsset


class  GenericAssetViewSet(PeCoReTModelViewSet):
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]
    api_scope = 'scope_all_projects'
    queryset = GenericAsset.objects.none()
    serializer_class = GenericAssetSerializer
    search_fields = ['name']

    def get_queryset(self):
        return GenericAsset.objects.for_project(self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project)
