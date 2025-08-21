from django.db import models
from pecoret.core.models import TimestampedModel


class PinnedProjectQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(project=project)

    def for_user(self, user):
        return self.filter(user=user)


class PinnedProject(TimestampedModel):
    objects = PinnedProjectQuerySet.as_manager()
    project = models.ForeignKey('backend.Project', on_delete=models.CASCADE)
    user = models.ForeignKey('backend.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ["-project__name"]
        unique_together = [
            ('project', 'user')
        ]
