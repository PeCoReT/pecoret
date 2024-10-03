from rest_framework import serializers

from attack_surface.models.target import Target, ScopeChoices, DataTypes
from pecoret.core.serializers import ValuedChoiceField, PrimaryKeyRelatedField
from .asn import ASNSerializer
from .program import ProgramSerializer


class MinimalTargetSerializer(serializers.ModelSerializer):
    scope = ValuedChoiceField(choices=ScopeChoices.choices, required=False)
    data_type = ValuedChoiceField(choices=DataTypes.choices, required=False)
    program = PrimaryKeyRelatedField(serializer=ProgramSerializer)
    asn = PrimaryKeyRelatedField(serializer=ASNSerializer, required=False, allow_null=True)

    class Meta:
        model = Target
        fields = ['pk', 'date_created', 'date_updated', 'data', 'scope', 'data_type', 'display_name', 'description',
                  'hostnames', 'resolved_ip', 'program', 'asn', 'date_asn_last_updated']


class TargetSerializer(MinimalTargetSerializer):
    class Meta:
        model = Target
        fields = MinimalTargetSerializer.Meta.fields
