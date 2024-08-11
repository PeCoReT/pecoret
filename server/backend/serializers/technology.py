from rest_framework import serializers

from backend.models import Technology
from pecoret.core.serializers import PrimaryKeyRelatedField


class ImplicitTechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = [
            'pk', 'name', 'vendor', 'cpe', 'description'
        ]


class FlatTechnologySerializer(serializers.ModelSerializer):
    source_code_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = Technology
        fields = [
            'pk', 'name', 'homepage', 'date_created', 'date_updated', 'vendor', 'cpe', 'description',
            'source_code_url', 'source_code_available'
        ]


class TechnologySerializer(FlatTechnologySerializer):
    implicit_technologies = PrimaryKeyRelatedField(serializer=ImplicitTechnologySerializer,
                                                   many=True, required=False, allow_empty=True, allow_null=True)

    class Meta:
        model = Technology
        fields = FlatTechnologySerializer.Meta.fields + ['implicit_technologies']
        extra_kwargs = {
            'cpe': {'allow_null': False, 'allow_blank': False},
            'vendor': {'allow_null': False, 'allow_blank': False},
        }
