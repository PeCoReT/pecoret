import base64
import uuid
from pathlib import Path
from django.urls import reverse
from pecoret.core.models import TimestampedModel
from django.db import models


def upload_path(instance, filename):
    """
    upload attachment path. generates uuid4 based filename.

    :param instance:
    :param filename:
    :return:
    """
    extension = Path(filename).suffix
    instance.name = filename
    return f"uploads/advisories/{instance.advisory.pk}/attachments/{uuid.uuid4()}{extension}"


class ImageAttachmentQuerySet(models.QuerySet):
    def for_advisory(self, advisory):
        return self.filter(advisory=advisory)


class ImageAttachment(TimestampedModel):
    objects = ImageAttachmentQuerySet.as_manager()
    advisory = models.ForeignKey('backend.Advisory', on_delete=models.CASCADE)
    image = models.ImageField(max_length=256, upload_to=upload_path)
    name = models.CharField(max_length=128)
    caption = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        ordering = ["-date_updated"]

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using=using, keep_parents=keep_parents)

    def get_preview_url(self):
        return reverse("advisories:attachment-preview", kwargs={
            'advisory': self.advisory.pk,
            'pk': self.pk
        })

    @property
    def image_base64(self):
        encoded = base64.b64encode(self.image.file.read())
        return f"data:image/png;base64,{encoded.decode()}"
