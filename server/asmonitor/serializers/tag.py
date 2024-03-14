from rest_framework import serializers
from asmonitor.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            'pk', 'name', 'color_rgb', 'description', 'color'
        ]
