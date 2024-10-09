from core.storage.viewset import ImageFileViewSet
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core import permissions


@extend_viewset_schema(tags=['Attack Surface'], verbose_name='image attachment')
class FindingImageViewSet(ImageFileViewSet):
    permission_classes = [
        permissions.GroupPermission(
            read_only_groups=[],
            read_write_groups=[permissions.Groups.GROUP_PENTESTER],
        )
    ]
    image_file_upload_directory = 'attack_surface'
