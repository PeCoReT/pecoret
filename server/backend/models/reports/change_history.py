from django.db import models


class ChangeHistoryManager(models.Manager):
    def for_project(self, project):
        return self.filter(report__project=project)


class ChangeHistory(models.Model):
    objects = ChangeHistoryManager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    version = models.FloatField()
    report = models.ForeignKey('backend.Report', on_delete=models.CASCADE)
    date = models.DateField()
    change = models.CharField(max_length=128)

    def __str__(self):
        return str(self.version)

    class Meta:
        unique_together = [
            ("report", "version")
        ]
        ordering = ["version"]
