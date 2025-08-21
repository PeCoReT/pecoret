from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django_q.models import Task as DjangoQTask
from pecoret.core.models import TimestampedModel


class ReleaseType(models.IntegerChoices):
    DRAFT = 0, "Draft"
    FINAL = 1, "Final"
    PREVIEW = 2, "Preview"


class ReportReleaseQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(report__project=project)

    def for_report(self, report):
        return self.filter(report=report)

    def preview(self):
        return self.filter(release_type=ReleaseType.PREVIEW)


class ReportRelease(TimestampedModel):
    objects = ReportReleaseQuerySet.as_manager()
    name = models.CharField(max_length=128)
    raw_source = models.TextField(blank=True, null=True)
    compiled_source = models.BinaryField(blank=True, null=True)
    release_type = models.PositiveSmallIntegerField(choices=ReleaseType.choices)
    task_id = models.CharField(max_length=64, null=True, blank=True)
    report = models.ForeignKey('backend.Report', on_delete=models.CASCADE)
    content_type = models.CharField(max_length=128, default="application/octet-stream")
    file_extension = models.CharField(max_length=12, default="pdf")

    def __str__(self):
        return self.name

    @property
    def task(self):
        try:
            return DjangoQTask.objects.get(pk=self.task_id)
        except DjangoQTask.DoesNotExist:
            return DjangoQTask.objects.none()

    def save(self, *args, **kwargs):
        """
        overwrite save method to perform clean

        :param args:
        :param kwargs:
        :return:
        """
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        """
        check if there is only one preview document, otherwise wipe ti
        :return:
        """
        if not self.pk:
            qs = ReportRelease.objects.for_report(self.report).filter(release_type=ReleaseType.PREVIEW)
            if qs.exists():
                # delete existing preview document
                qs.delete()
        # check if report template exists
        if self.report.template not in list(settings.REPORT_TEMPLATES.keys()):
            raise ValidationError({'report': 'Report template does not exist!'})
        return super().clean()
