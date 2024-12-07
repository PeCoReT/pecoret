from rest_framework import serializers

from core.custom_fields.models import CustomField, FieldTypeChoices
from pecoret.core.serializers import ValuedChoiceField


class CustomFieldSerializer(serializers.ModelSerializer):
    field_type = ValuedChoiceField(FieldTypeChoices.choices)

    class Meta:
        model = CustomField
        fields = [
            'pk', 'name', 'label', 'help_text', 'field_type', 'ordering', 'required', 'allow_markdown',
            'date_created', 'date_updated'
        ]
