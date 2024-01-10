from django.db import models
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class ReportVariant(models.IntegerChoices):
    PENTEST_PDF_REPORT = 0, "Pentest PDF"
    VULNERABILITY_CSV_REPORT = 1, "Vulnerability CSV"
    PENTEST_EXCEL = 2, "Pentest Excel"

    @property
    def to_plugin_method(self):
        """required to receive the required class of the variant

        Returns:
            str: class name (e.g. PentestPDFReport)
        """
        mappers = {
            'Pentest PDF': 'export_project_pdf_report',
            'Vulnerability CSV': 'export_vulnerability_csv',
            'Pentest Excel': 'export_project_excel'
        }
        return mappers[self._label_]


class ReportQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(project=project)

    def for_projects(self, projects):
        return self.filter(project_pk__in=projects.values("pk"))


class Report(models.Model):
    objects = ReportQuerySet.as_manager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=128)
    title = models.CharField(max_length=128, default="Pentest Report")
    project = models.ForeignKey('backend.Project', on_delete=models.CASCADE)
    author = models.ForeignKey('backend.User', on_delete=models.PROTECT)
    variant = models.PositiveSmallIntegerField(choices=ReportVariant.choices)
    recommendation = models.TextField(null=True, blank=True)
    evaluation = models.TextField(null=True, blank=True)
    template = models.ForeignKey('backend.ReportTemplate', on_delete=models.PROTECT)

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

    def clean(self):
        try:
            instance = Report.objects.get(pk=self.pk)
            if instance.variant != self.variant:
                raise ValidationError(
                    {"variant": "Report variant cannot be changed after creation!"}
                )
        except ObjectDoesNotExist:
            pass
        return super().clean()

    class Meta:
        ordering = ["-date_created"]
