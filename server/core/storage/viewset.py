from django.core.exceptions import ImproperlyConfigured

from core.storage.models import ImageFile
from core.storage.serializers import ImageFileSerializer
from pecoret.core.viewsets import GenericViewSet
from pecoret.core.mixins import CreateModelMixin


class ImageFileViewSet(CreateModelMixin, GenericViewSet):
    queryset = ImageFile.objects.none()
    serializer_class = ImageFileSerializer
    image_file_upload_directory = None

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['image_file_upload_directory'] = self.get_image_file_upload_directory()
        return context

    def get_image_file_upload_directory(self):
        if not self.image_file_upload_directory:
            raise ImproperlyConfigured('no image_file_upload_directory set')
        return self.image_file_upload_directory
