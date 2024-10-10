from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema, extend_schema_view

from core.storage.models import ImageFile
from core.storage.viewset import ImageFileViewSet
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema


@extend_schema_view(preview=extend_schema(tags=['Advisories'], operation_id='Image Attachments'))
@extend_viewset_schema(tags=['Advisories'], verbose_name='image attachment')
class ImageAttachmentViewSet(ImageFileViewSet):
    search_fields = ["caption"]
    image_file_upload_directory = 'advisories'
    permission_classes = [
        permissions.GroupPermission(
            read_only_groups=[],
            read_write_groups=[permissions.Groups.GROUP_PENTESTER],
        )
    ]

    def get_queryset(self):
        return ImageFile.objects.for_linked_object('advisories', 'advisory', self.kwargs.get('advisory'))

    def perform_create(self, serializer):
        ct = ContentType.objects.get(app_label='advisories', model='advisory')
        serializer.save(content_type=ct, object_id=self.kwargs.get('advisory'))
