from django.db import models
from pecoret.core.models import PeCoReTBaseModel


class ScopePermission(models.IntegerChoices):
    DENIED = 0, "Denied"
    ALLOWED = 1, "Allowed"


class ProjectScopeQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(project=project)

    def allowed(self):
        return self.filter(permission=ScopePermission.ALLOWED)

    def forbidden(self):
        return self.filter(permission=ScopePermission.DENIED)


class ProjectScope(PeCoReTBaseModel):
    objects = ProjectScopeQuerySet.as_manager()
    project = models.ForeignKey('backend.Project', on_delete=models.CASCADE)
    permission = models.PositiveSmallIntegerField(choices=ScopePermission.choices)
    details = models.CharField(max_length=256)

    class Meta:
        ordering = ["pk"]
