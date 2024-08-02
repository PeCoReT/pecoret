from django.http import FileResponse
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core.utils.schema import extend_viewset_schema
from advisories.models.attachment import ImageAttachment
from advisories.serializers.attachment import ImageAttachmentSerializer


@extend_schema_view(preview=extend_schema(tags=['Advisories'], operation_id='Image Attachments'))
@extend_viewset_schema(tags=['Advisories'], verbose_name='image attachment')
class ImageAttachmentViewSet(PeCoReTModelViewSet):
    queryset = ImageAttachment.objects.none()
    search_fields = ["caption"]
    serializer_class = ImageAttachmentSerializer
    permission_classes = [
        permissions.GroupPermission(
            read_only_groups=[],
            read_write_groups=[permissions.Groups.GROUP_PENTESTER],
        )
    ]

    def get_queryset(self):
        return ImageAttachment.objects.for_advisory(self.kwargs.get('advisory'))

    def perform_create(self, serializer):
        serializer.save(advisory_id=self.kwargs.get('advisory'))

    @action(methods=['get'], detail=True)
    def preview(self, *args, **kwargs):
        instance = self.get_object()
        file_handle = instance.image.open()
        response = FileResponse(file_handle)
        return response
