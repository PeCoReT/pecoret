from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pecoret.core.models import TimestampedModel


FIELD_MAP = {
    'char': serializers.CharField,
    'text': serializers.CharField,
    'integer': serializers.IntegerField,
}


class FieldTypeChoices(models.IntegerChoices):
    CHAR = 0, "char"
    TEXT = 1, "text"
    INTEGER = 2, "integer"


class CustomFieldQuerySet(models.query.QuerySet):
    pass


class CustomField(TimestampedModel):
    """
    defines a custom field for a model. this is abstract.
    if you want to use it, subclass this and implement your own.
    inspired and some parts borrowed from
    https://github.com/django-helpdesk/django-helpdesk/blob/main/helpdesk/models.py
    """
    objects = CustomFieldQuerySet.as_manager()
    name = models.CharField(unique=True, max_length=255, help_text="the name of the field")
    label = models.CharField(max_length=255, help_text="the display label for the field")
    help_text = models.TextField(help_text="shown as help text on the field", blank=True, null=True)
    field_type = models.PositiveIntegerField(choices=FieldTypeChoices.choices)
    max_length = models.PositiveIntegerField(blank=True, null=True, help_text="the maximum chars of the field")
    required = models.BooleanField(default=False, help_text="whether the field is required")
    allow_markdown = models.BooleanField(default=False, help_text="whether the field is allowed to be markdown")

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

    def get_serializer_fields(self):
        pass

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        if self.allow_markdown and self.field_type not in [FieldTypeChoices.TEXT]:
            raise ValidationError({'allow_markdown': 'Markdown is not supported for this field type.'})
        return super().clean()
