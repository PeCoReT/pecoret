from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pecoret.core.models import TimestampedModel


FIELD_MAP = {
    'char': serializers.CharField,
    'text': serializers.CharField,
    'integer': serializers.IntegerField,
    'ip': serializers.IPAddressField,
    'url': serializers.URLField,
}


class FieldTypeChoices(models.IntegerChoices):
    CHAR = 0, "char"
    TEXT = 1, "text"
    INTEGER = 2, "integer"
    IP = 3, "ip"
    URL = 4, "url"


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
    ordering = models.PositiveIntegerField(default=5, help_text="the ordering of the field")

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['ordering']

    @staticmethod
    def get_serializer_map():
        return FIELD_MAP

    @staticmethod
    def get_field_type_choices():
        return FieldTypeChoices

    def get_serializer_field(self):
        field = self.get_serializer_map()[FieldTypeChoices(self.field_type).label]
        attributes = {
            'label': self.label,
            'help_text': self.help_text,
            'required': self.required,
            'allow_null': not self.required,
        }
        if self.max_length:
            attributes['max_length'] = self.max_length
        return field(**attributes)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        if self.allow_markdown and self.field_type not in [FieldTypeChoices.TEXT]:
            raise ValidationError({'allow_markdown': 'Markdown is not supported for this field type.'})
        return super().clean()


class CustomFieldValue(TimestampedModel):
    value = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        serializer_field = self.field.get_serializer_field()
        serializer_field.run_validation(self.value)
        return super().clean()
