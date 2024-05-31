from rest_framework import serializers
from attack_surface.models.target import Target, ScopeChoices, DataTypes
from pecoret.core.serializers import ValuedChoiceField, PrimaryKeyRelatedField
from backend.serializers.technology import TechnologySerializer
from .program import ProgramSerializer
from .tag import TagSerializer


class TargetSerializer(serializers.ModelSerializer):
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)
    scope = ValuedChoiceField(choices=ScopeChoices.choices, required=False)
    data_type = ValuedChoiceField(choices=DataTypes.choices)
    tags = PrimaryKeyRelatedField(serializer=TagSerializer, many=True, required=False)
    technologies = PrimaryKeyRelatedField(serializer=TechnologySerializer, many=True, required=False)

    class Meta:
        model = Target
        fields = [
            'date_created', 'date_updated', 'pk', 'first_seen', 'last_seen', 'data', 'scope', 'tags',
            'program', 'description', 'technologies', 'data_type'
        ]
