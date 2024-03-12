from rest_framework import serializers
from backend.models import Technology


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = [
            'pk', 'name', 'homepage', 'date_created', 'date_updated',
            'cpe', 'description'
        ]
