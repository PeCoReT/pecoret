from django.db import models


class AccountQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(project=project)

    def is_compromised(self):
        return self.filter(compromised=True)


class Account(models.Model):
    objects = AccountQuerySet.as_manager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(
        "backend.Project", on_delete=models.CASCADE, editable=False
    )
    role = models.CharField(max_length=256, blank=True)
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256, blank=True)
    accessible = models.BooleanField(null=True, blank=True)
    compromised = models.BooleanField(default=False, blank=True)
    description = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        ordering = ("-pk",)

    def __str__(self):
        return self.username
