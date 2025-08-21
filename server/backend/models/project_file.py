import uuid
from pathlib import Path
from django.db import models
from pecoret.core.models import TimestampedModel


class ProjectFileQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(project=project)


def project_file_path(instance, filename):
    return f"uploads/projects/{instance.project.pk}/files/{uuid.uuid4()}{Path(filename).suffix}"


class ProjectFile(TimestampedModel):
    objects = ProjectFileQuerySet.as_manager()
    project = models.ForeignKey('backend.Project', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=project_file_path)

    class Meta:
        ordering = ["name"]
        unique_together = [
            ('project', 'name')
        ]

    def delete(self, using=None, keep_parents=False):
        # ensure file on disk is deleted too
        self.file.delete()
        super().delete(using=using, keep_parents=keep_parents)
