from rest_framework import serializers

from attack_surface.models.target import Target, ScopeChoices, DataTypes
from pecoret.core.serializers import ValuedChoiceField, PrimaryKeyRelatedField
from .host import HostSerializer
from .program import ProgramSerializer


class MinimalTargetSerializer(serializers.ModelSerializer):
    scope = ValuedChoiceField(choices=ScopeChoices.choices, required=False)
    data_type = ValuedChoiceField(choices=DataTypes.choices, required=False)
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)

    class Meta:
        model = Target
        fields = ['pk', 'date_created', 'date_updated', 'data', 'scope', 'data_type', 'display_name', 'description',
                  'program']


class TargetSerializer(MinimalTargetSerializer):
    host = PrimaryKeyRelatedField(serializer=HostSerializer, required=False)

    class Meta:
        model = Target
        fields = MinimalTargetSerializer.Meta.fields + ['host']
