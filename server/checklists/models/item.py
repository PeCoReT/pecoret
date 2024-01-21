from django.db import models
from django.core.validators import RegexValidator
from pecoret.core.models import PeCoReTBaseModel, TimestampedModel


ID_REGEX = r'^[\w\d_-]*$'


class ItemStatus(models.IntegerChoices):
    OPEN = 0, "Open"
    CLOSED = 1, "Closed"


class BaseItemQuerySet(models.QuerySet):
    def for_category(self, category):
        return self.filter(category=category)


class BaseItem(PeCoReTBaseModel, TimestampedModel):
    objects = BaseItemQuerySet.as_manager()
    name = models.CharField(max_length=128)
    item_id = models.CharField(max_length=128, validators=[RegexValidator(regex=ID_REGEX)])
    description = models.TextField()
    category = models.ForeignKey("checklists.Category", on_delete=models.CASCADE)

    class Meta:
        ordering = ["item_id"]
        abstract = True
        unique_together = [("category", "item_id")]

    def __str__(self):
        return self.name


class Item(BaseItem):
    """this is the model that is used for templating tasks.
    Once a category item is mapped to an asset, it becomes a task
    """


class AssetItemQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(project=project)

    def for_category(self, category):
        return self.filter(category=category)

    def open(self):
        return self.filter(status=ItemStatus.OPEN)

    def closed(self):
        return self.filter(status=ItemStatus.CLOSED)


class AssetItem(BaseItem):
    objects = AssetItemQuerySet.as_manager()
    category = models.ForeignKey("checklists.AssetCategory", on_delete=models.CASCADE)
    project = models.ForeignKey('backend.Project', on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=ItemStatus.choices, default=ItemStatus.OPEN)
