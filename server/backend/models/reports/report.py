from django.db import models
from pecoret.reporting.utils import get_report_template_choices


class ReportQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(project=project)


class Report(models.Model):
    objects = ReportQuerySet.as_manager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=128)
    title = models.CharField(max_length=128, default="Pentest Report")
    project = models.ForeignKey('backend.Project', on_delete=models.CASCADE)
    recommendation = models.TextField(null=True, blank=True)
    evaluation = models.TextField(null=True, blank=True)
    template = models.CharField(max_length=128, choices=get_report_template_choices)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_next_minor_version(self):
        if not self.changehistory_set.count():
            return "0.1"
        return self.changehistory_set.first().version + 0.1

    def get_current_version(self):
        if not self.changehistory_set.count():
            return "0.1"
        return self.changehistory_set.first().version

    class Meta:
        ordering = ["-date_created"]
