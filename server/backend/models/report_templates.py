from pathlib import Path
from django.db import models


class ReportTemplateStatus(models.IntegerChoices):
    ACTIVE = 0, "Active"
    DRAFT = 1, "Draft"
    DEACTIVATED = 2, "Deactivated"


class ReportTemplateQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=ReportTemplateStatus.ACTIVE)


class ReportTemplate(models.Model):
    objects = ReportTemplateQuerySet.as_manager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=ReportTemplateStatus.choices,
                                              default=ReportTemplateStatus.ACTIVE)
    name = models.CharField(max_length=64, unique=True)
    package = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    @property
    def template_path(self):
        return str(Path(self.package) / "templates/")

    class Meta:
        ordering = ["-date_created", "name"]
