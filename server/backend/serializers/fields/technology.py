from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from backend.models.technology import Technology


@extend_schema_field(OpenApiTypes.INT)
class TechnologyField(serializers.Field):
    default_error_messages = {
        'invalid_pk': 'invalid value'
    }

    def to_internal_value(self, data):
        qs = Technology.objects.filter(pk=data)
        if qs.exists():
            return qs.get()
        self.fail('invalid_pk')

    def to_representation(self, value):
        return value.pk
