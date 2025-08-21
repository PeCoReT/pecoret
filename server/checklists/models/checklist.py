from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

from pecoret.core.models import PeCoReTBaseModel
from .category import AssetCategory
from .item import AssetItem, Item

ID_REGEX = r'^[\w\d_-]*$'


class BaseChecklist(PeCoReTBaseModel):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=128)
    checklist_id = models.CharField(max_length=128, unique=True, validators=[RegexValidator(regex=ID_REGEX)])
    categories = models.ManyToManyField("checklists.Category")

    class Meta:
        ordering = ["checklist_id"]
        abstract = True

    def __str__(self):
        return self.name


class Checklist(BaseChecklist):
    pass


class AssetChecklistQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(project=project)

    def with_asset(self, asset):
        return self.filter(asset=asset)


class AssetChecklistManager(models.Manager):
    def create_from_checklist(self, **data):
        default_fields = [
            "name",
            "checklist_id",
        ]
        check = Checklist.objects.get(checklist_id=data["checklist_id"])
        for field in default_fields:
            data.setdefault(field, getattr(check, field))
        checklist = self.create(**data)
        for category in check.categories.all():
            asset_category, _created = AssetCategory.objects.get_or_create(
                project=checklist.project,
                name=category.name,
                summary=category.summary,
                category_id=category.category_id,
            )
            checklist.categories.add(asset_category)
            for item in Item.objects.for_category(category):
                AssetItem.objects.get_or_create(
                    project=checklist.project,
                    name=item.name,
                    item_id=item.item_id,
                    description=item.description,
                    category=asset_category,
                )
        return checklist


class AssetChecklist(BaseChecklist):
    project = models.ForeignKey(
        "backend.Project", editable=False, on_delete=models.CASCADE
    )
    checklist_id = models.CharField(max_length=128)
    asset = models.ForeignKey('backend.Asset', on_delete=models.CASCADE)
    objects = AssetChecklistManager.from_queryset(AssetChecklistQuerySet)()
    categories = models.ManyToManyField("checklists.AssetCategory")

    class Meta:
        ordering = ["checklist_id"]

    @property
    def open_item_count(self):
        return AssetItem.objects.for_category(
            models.Subquery(self.categories.values("pk"))
        ).open().count()

    @property
    def closed_item_count(self):
        return AssetItem.objects.for_category(
            models.Subquery(self.categories.values('pk'))
        ).closed().count()

    def clean(self):
        if AssetChecklist.objects.filter(checklist_id=self.checklist_id).with_asset(
                self.asset).exists():
            raise ValidationError({'asset': "checklist already exist for this asset"})
        return super().clean()
