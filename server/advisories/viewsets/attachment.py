from django.http import FileResponse
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet
from pecoret.core.utils.schema import extend_viewset_schema
from advisories.models.attachment import ImageAttachment
from advisories.serializers.attachment import ImageAttachmentSerializer
from advisories.models.advisory_membership import Roles


@extend_schema_view(preview=extend_schema(tags=['Advisories'], operation_id='Image Attachments'))
@extend_viewset_schema(tags=['Advisories'], verbose_name='image attachment')
class ImageAttachmentViewSet(PeCoReTModelViewSet):
    queryset = ImageAttachment.objects.none()
    search_fields = ["caption"]
    serializer_class = ImageAttachmentSerializer
    permission_classes = [
        permissions.AdvisoryPermission(
            read_write_roles=[Roles.CREATOR, Roles.VENDOR],
            read_only_roles=[Roles.READ_ONLY],
        )
    ]

    def get_queryset(self):
        return ImageAttachment.objects.for_advisory(self.request.advisory)

    def perform_create(self, serializer):
        serializer.save(advisory=self.request.advisory)

    @action(methods=['get'], detail=True)
    def preview(self, *args, **kwargs):
        instance = self.get_object()
        file_handle = instance.image.open()
        response = FileResponse(file_handle)
        return response
