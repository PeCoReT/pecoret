from django.db import models


class FindingTimelineQuerySet(models.QuerySet):
    def for_finding(self, finding):
        return self.filter(finding=finding)

    def for_project(self, project):
        return self.filter(finding__project=project)


class TimelineItem(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('backend.User', on_delete=models.SET_NULL, null=True)
    is_system_log = models.BooleanField(default=False)
    title = models.CharField(max_length=128)
    text = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-date_created"]
        abstract = True


class FindingTimeline(TimelineItem):
    objects = FindingTimelineQuerySet.as_manager()
    finding = models.ForeignKey('backend.Finding', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} on {self.finding.unique_id}"
