from django.db import models
from pecoret.core.models import TimestampedModel


class ProjectNoteQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(project=project)


class ProjectNote(TimestampedModel):
    objects = ProjectNoteQuerySet.as_manager()
    project = models.ForeignKey('backend.Project', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = models.TextField(default="")

    class Meta:
        ordering = ["title"]
        unique_together = [
            ('project', 'title')
        ]
