import base64
import secrets
import uuid
from pathlib import Path

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from pecoret.core.models import TimestampedModel
from django.db import models


def upload_path(instance, filename):
    """
    upload image file. generates uuid4 based filename.

    :param instance:
    :param filename:
    :return:
    """
    extension = Path(filename).suffix
    instance.name = filename
    rand = secrets.token_hex(8)
    directory = instance.upload_directory
    if instance.object_id:
        directory = f'{directory}/{instance.object_id}'
    return f"uploads/{directory}/images/{instance.pk}-{rand}{extension}"


class ImageFileQuerySet(models.QuerySet):
    def for_linked_object(self, app_label, model_name, pk):
        ct = ContentType.objects.get(app_label=app_label, model=model_name)
        return self.filter(content_type=ct, object_id=pk)


class ImageFile(TimestampedModel):
    objects = ImageFileQuerySet.as_manager()
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(max_length=256, upload_to=upload_path)
    name = models.CharField(max_length=128)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    linked_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ["-date_updated"]

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using=using, keep_parents=keep_parents)

    @property
    def storage_link(self):
        return f'storage://{self.image.url}'

    @property
    def image_base64(self):
        encoded = base64.b64encode(self.image.file.read())
        return f"data:image/png;base64,{encoded.decode()}"
