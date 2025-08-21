from pathlib import Path
from django.db import models
from pecoret.reporting.utils import get_report_template_choices


def upload_path(instance, filename):
    extension = Path(filename).suffix
    return f"uploads/companies/{instance.pk}/logo{extension}"


class CompanyQuerySet(models.QuerySet):
    def for_project_ids(self, project_ids):
        return self.filter(project__pk__in=project_ids)

    def for_user(self, user):
        if user.is_customer:
            return self.filter(pk=user.company.pk)
        return self.all()


class Company(models.Model):
    objects = CompanyQuerySet.as_manager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=256)
    street = models.CharField(max_length=256)
    zipcode = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    report_template = models.CharField(max_length=256, choices=get_report_template_choices)
    logo = models.ImageField(max_length=256, upload_to=upload_path, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def has_logo(self):
        if self.logo:
            return True
        return False
