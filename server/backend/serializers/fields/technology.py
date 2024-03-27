from rest_framework import serializers
from backend.models.technology import Technology


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
