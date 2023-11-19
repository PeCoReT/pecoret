from django.db import models
from django.conf import settings
from pecoret.core.models import TimestampedModel


class ProjectStatus(models.IntegerChoices):
    OPEN = 0, "Open"
    CLOSED = 1, "Closed"


class TestMethod(models.IntegerChoices):
    WHITE_BOX = 0, "White Box"
    GREY_BOX = 1, "Grey Box"
    BLACK_BOX = 2, "Black Box"
    UNKNOWN = 3, "Unknown"


class ScoreChoices(models.IntegerChoices):
    CVSS4_BASE = 0, 'CVSS 4.0 Base'
    CVSS31_BASE = 1, 'CVSS 3.1 Base'


class ProjectQuerySet(models.QuerySet):
    def for_project(self, project):
        if hasattr(project, "pk"):
            project = project.pk
        return self.filter(pk=project)

    def for_user(self, user):
        return self.filter(membership__user=user)

    def closed(self):
        return self.filter(status=ProjectStatus.CLOSED)

    def open(self):
        return self.filter(status=ProjectStatus.OPEN)


class Project(TimestampedModel):
    objects = ProjectQuerySet.as_manager()
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.CharField(max_length=254, unique=True)
    pentest_types = models.ManyToManyField("backend.PentestType")
    description = models.TextField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        choices=ProjectStatus.choices, default=ProjectStatus.OPEN
    )
    company = models.ForeignKey("backend.Company", on_delete=models.PROTECT)
    test_method = models.PositiveSmallIntegerField(choices=TestMethod.choices)
    year = models.PositiveIntegerField(editable=False, blank=True, null=True)
    require_cvss_score = models.PositiveSmallIntegerField(blank=True, null=True, choices=ScoreChoices.choices)
    language = models.CharField(choices=settings.LANGUAGES, default="en", max_length=4)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.year = self.start_date.year
        super().save(*args, **kwargs)
