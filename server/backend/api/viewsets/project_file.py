import os
from django.http import FileResponse
from rest_framework.decorators import action
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet
from backend.api.serializers.project_file import ProjectFileSerializer
from backend.models.project_file import ProjectFile
from pecoret.core.utils.schema import extend_viewset_schema, extend_schema_view, extend_schema


@extend_viewset_schema(tags=['Projects'], verbose_name='project file')
@extend_schema_view(download=extend_schema(tags=['Projects'], operation_id='Download project file'))
class ProjectFileViewSet(PeCoReTModelViewSet):
    queryset = ProjectFile.objects.none()
    search_fields = ["name"]
    api_scope = "scope_all_projects"
    serializer_class = ProjectFileSerializer
    permission_classes = [permissions.PRESET_PENTESTER_OR_READONLY]

    def get_queryset(self):
        return ProjectFile.objects.for_project(self.request.project)

    def perform_create(self, serializer):
        serializer.save(project=self.request.project)

    @action(methods=['get'], detail=True)
    def download(self, *args, **kwargs):
        instance = self.get_object()
        # get an open file handle (I'm just using a file attached to the model for this example):
        file_handle = instance.file.open()

        # send file
        response = FileResponse(file_handle, content_type='application/octet-stream')
        response['Content-Length'] = instance.file.size
        response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(instance.file.name)
        return response
