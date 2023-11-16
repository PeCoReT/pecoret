import base64
import uuid
from pathlib import Path
from django.urls import reverse
from pecoret.core.models import TimestampedModel
from django.db import models


def finding_upload_path(instance, filename):
    """
    upload finding attachment path. generates uuid4 based filename.

    :param instance:
    :param filename:
    :return:
    """
    extension = Path(filename).suffix
    instance.name = filename
    return f"uploads/projects/{instance.finding.project.pk}/findings/{instance.finding.pk}/attachments/{uuid.uuid4()}{extension}"


class FindingImageAttachmentQuerySet(models.QuerySet):
    def for_finding(self, finding):
        return self.filter(finding=finding)

    def for_project(self, project):
        return self.filter(finding__project=project)


class FindingImageAttachment(TimestampedModel):
    objects = FindingImageAttachmentQuerySet.as_manager()
    finding = models.ForeignKey('backend.Finding', on_delete=models.CASCADE)
    image = models.ImageField(max_length=256, upload_to=finding_upload_path)
    name = models.CharField(max_length=128)

    class Meta:
        ordering = ["-date_updated"]

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using=using, keep_parents=keep_parents)

    def get_preview_url(self):
        return reverse("backend:findings:attachment-preview", kwargs={
            'project': self.finding.project.pk,
            'finding': self.finding.pk, 'pk': self.pk})

    @property
    def image_base64(self):
        encoded = base64.b64encode(self.image.file.read())
        return f"data:image/png;base64,{encoded.decode()}"
