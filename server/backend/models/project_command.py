from django.db import models
from django.utils import timezone
from pecoret.core.models import PeCoReTBaseModel


class ProjectCommandQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(project=project)


class ProjectCommand(PeCoReTBaseModel):
    objects = ProjectCommandQuerySet.as_manager()
    project = models.ForeignKey('backend.Project', on_delete=models.CASCADE)
    user = models.ForeignKey('backend.User', on_delete=models.SET_NULL, null=True)
    command = models.CharField(max_length=512)
    date_run = models.DateTimeField(default=timezone.now)
    output = models.TextField()

    class Meta:
        ordering = ["project", "date_run"]
