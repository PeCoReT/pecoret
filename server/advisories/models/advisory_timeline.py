from django.db import models


class AdvisoryTimelineQuerySet(models.QuerySet):
    def for_advisory(self, advisory):
        return self.filter(advisory=advisory)


class AdvisoryTimeline(models.Model):
    objects = AdvisoryTimelineQuerySet.as_manager()
    date = models.DateField()
    text = models.CharField(max_length=255)
    advisory = models.ForeignKey('advisories.Advisory', on_delete=models.CASCADE)

    class Meta:
        ordering = ["-date"]
        db_table = "backend_advisorytimeline"
