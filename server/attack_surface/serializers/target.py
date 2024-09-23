from rest_framework import serializers
from attack_surface.models.target import Target, ScopeChoices, DataTypes
from pecoret.core.serializers import ValuedChoiceField, PrimaryKeyRelatedField
from .host import HostSerializer
from .program import ProgramSerializer


class TargetSerializer(serializers.ModelSerializer):
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)
    scope = ValuedChoiceField(choices=ScopeChoices.choices, required=False)
    data_type = ValuedChoiceField(choices=DataTypes.choices)
    host = PrimaryKeyRelatedField(serializer=HostSerializer, required=False)

    class Meta:
        model = Target
        fields = [
            'date_created', 'date_updated', 'pk', 'data', 'scope',
            'program', 'description', 'data_type', 'host', 'display_name'
        ]
