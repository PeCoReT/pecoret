import base64
import secrets
import uuid
from pathlib import Path
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
    return f"uploads/{instance.upload_directory}/images/{instance.pk}-{rand}{extension}"


class ImageFile(TimestampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(max_length=256, upload_to=upload_path)
    name = models.CharField(max_length=128)

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
