from django.db import models


class CompanyContactQuerySet(models.QuerySet):

    def for_project(self, project):
        return self.filter(project_contacts__project=project)

    def for_company(self, company):
        return self.filter(company=company)


class CompanyContact(models.Model):
    objects = CompanyContactQuerySet.as_manager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    company = models.ForeignKey('backend.Company', on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=28)
    role = models.CharField(max_length=128)
    pgp_public_key = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = [
            ("first_name", "last_name", "company")
        ]
        ordering = ["first_name", "last_name"]
