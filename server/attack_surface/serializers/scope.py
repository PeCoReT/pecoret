from rest_framework import serializers

from attack_surface.models import Scope, ScopeItem
from attack_surface.serializers.program import ProgramSerializer
from pecoret.core.serializers import PrimaryKeyRelatedField


class ScopeSerializer(serializers.ModelSerializer):
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)

    class Meta:
        model = Scope
        fields = [
            'pk', 'date_created', 'date_updated',
            'program', 'name'
        ]
