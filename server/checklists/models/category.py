from django.core.validators import RegexValidator
from django.db import models
from pecoret.core.models import PeCoReTBaseModel, TimestampedModel


ID_REGEX = r'^[\w\d_-]*$'


class BaseCategory(PeCoReTBaseModel, TimestampedModel):
    name = models.CharField(max_length=128)
    summary = models.CharField(max_length=258, null=True, blank=True)
    category_id = models.CharField(max_length=128, validators=[RegexValidator(ID_REGEX)])

    class Meta:
        ordering = ["category_id"]
        verbose_name_plural = "Categories"
        abstract = True

    def __str__(self):
        return self.name


class Category(BaseCategory):
    """this is the first abstraction layer of the checklist.
    It can be included in many checklists and consists of a set
    of items.
    """
    category_id = models.CharField(max_length=128, unique=True)


class AssetCategoryQuerySet(models.QuerySet):
    def for_checklist(self, checklist):
        return self.filter(assetchecklist=checklist)

    def for_project(self, project):
        return self.filter(project=project)


class AssetCategory(BaseCategory):
    objects = AssetCategoryQuerySet.as_manager()
    project = models.ForeignKey('backend.Project', on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('category_id', 'project')
        ]
