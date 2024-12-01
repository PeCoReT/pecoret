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


class CustomFieldRelatedSerializer(serializers.ModelSerializer):
    """
    a serializer that is used by objects that have related custom fields e.g. assets
    """

    def get_custom_field_class(self):
        raise Exception("Not implemented")

    def get_custom_field_value_class(self):
        raise Exception("Not implemented")

    def get_custom_field_queryset(self):
        """ get the queryset for the custom field model .e.g CustomFieldAsset.objects.all()"""
        return self.get_custom_field_class().objects.all()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for every custom field, create a valid SerializerField
        for field in self.get_custom_field_queryset():
            self.fields[f'custom_{field.name}'] = field.get_serializer_field()
            if self.instance:
                if isinstance(self.instance, list):
                    for instance in self.instance:
                        value = self.get_custom_field_value(instance, field)
                        setattr(instance, f'custom_{field.name}', value)
                else:
                    value = self.get_custom_field_value(self.instance, field)
                    setattr(self.instance, f'custom_{field.name}', value)

    def get_value_serializer_class(self):
        raise Exception("Not implemented")

    def to_representation(self, value):
        representation = super().to_representation(value)
        for key, field_value in self.fields.items():
            if key.startswith('custom_'):
                representation[key] = self.get_value_serializer_class()(instance=getattr(value, key, None)).data
        return representation

    def get_custom_field_value(self, instance, field):
        try:
            value = self.get_custom_field_value_class().objects.for_asset(instance).get(field=field)
        except self.get_custom_field_class().DoesNotExist:
            value = None
        return value

    def create(self, validated_data):
        custom_fields = {}
        for field in self.get_custom_field_queryset():
            custom_fields[field.pk] = validated_data.pop(f'custom_{field.name}', None)
        instance = super().create(validated_data)
        for field_pk, value in custom_fields.items():
            try:
                # get custom field if one exists and populate it
                custom_field = self.get_custom_field_class().objects.get(pk=field_pk)
            except self.get_custom_field_class().DoesNotExist:
                # if no custom asset field exists, continue
                continue
            self.get_custom_field_value_class().objects.create(asset=instance, field=custom_field, value=value)
            setattr(instance, f'custom_{custom_field.name}', value)
        return instance

    def update(self, instance, validated_data):
        custom_fields = {}
        for field in self.get_custom_field_queryset():
            custom_fields[field.pk] = validated_data.pop(f'custom_{field.name}', None)
        instance = super().update(instance, validated_data)
        for field_pk, value in custom_fields.items():
            try:
                custom_field = self.get_custom_field_class().objects.get(pk=field_pk)
            except self.get_custom_field_class().DoesNotExist:
                # if no custom asset field exists, continue
                continue
            self.get_custom_field_value_class().objects.update_or_create(
                asset=instance, field=custom_field, defaults={"value": value})
            setattr(instance, f'custom_{custom_field.name}', value)
        return instance
