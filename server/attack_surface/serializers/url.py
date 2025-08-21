from rest_framework import serializers

from attack_surface.models.url import URL
from backend.api.serializers.technology import FlatTechnologySerializer
from pecoret.core.serializers import PrimaryKeyRelatedField
from .service import ServiceSerializer
from .tag import TagSerializer


class URLSerializer(serializers.ModelSerializer):
    technologies = PrimaryKeyRelatedField(serializer=FlatTechnologySerializer, many=True, required=False)
    tags = PrimaryKeyRelatedField(serializer=TagSerializer, many=True, required=False)
    service = PrimaryKeyRelatedField(serializer=ServiceSerializer)

    class Meta:
        model = URL
        fields = [
            'pk', 'date_created', 'date_updated', 'status_code', 'service',
            'fuzzy_hash_body', 'fuzzy_hash_headers', 'response', 'is_base', 'tags', 'technologies', 'url',
            'display_name', 'is_in_scope', 'body_hash', 'title'
        ]
