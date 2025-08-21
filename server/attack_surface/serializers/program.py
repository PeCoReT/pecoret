from rest_framework import serializers
from attack_surface.models.program import Program


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = [
            'pk', 'name', 'description', 'date_created', 'date_updated'
        ]
