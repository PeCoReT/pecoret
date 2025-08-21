from django.db import models
from pecoret.core.models import TimestampedModel, PeCoReTBaseModel, CASCADE_USER_TO_GHOST


class CompanyInformationQuerySet(models.QuerySet):
    def for_company(self, company):
        return self.filter(company=company)


class CompanyInformation(TimestampedModel, PeCoReTBaseModel):
    objects = CompanyInformationQuerySet.as_manager()
    company = models.ForeignKey('backend.Company', on_delete=models.PROTECT)
    user = models.ForeignKey('backend.User', on_delete=CASCADE_USER_TO_GHOST)
    user_edit = models.ForeignKey('backend.User', null=True, blank=True, on_delete=CASCADE_USER_TO_GHOST,
                                  related_name='companyinformation_user_edit_set')
    text = models.TextField()

