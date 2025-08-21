from django.db import models
from pecoret.core.models import TimestampedModel


class ProjectContactManager(models.Manager):
    def for_project(self, project):
        return self.filter(project=project)


class ProjectContact(TimestampedModel):
    objects = ProjectContactManager()
    contact = models.ForeignKey('backend.CompanyContact', on_delete=models.PROTECT)
    project = models.ForeignKey('backend.Project', on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date_created", "-date_updated"]
        unique_together = [
            ("contact", "project")
        ]
