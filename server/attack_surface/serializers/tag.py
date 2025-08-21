from rest_framework import serializers
from attack_surface.models import Tag


class TagSerializer(serializers.ModelSerializer):
    color = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Tag
        fields = [
            'pk', 'name', 'description', 'color'
        ]
