from rest_framework import serializers
from attack_surface.models.finding_component import ComponentStatus, FindingComponent
from attack_surface.serializers.finding import FindingSerializer
from pecoret.core.serializers import ValuedChoiceField, PrimaryKeyRelatedField


class FindingComponentSerializer(serializers.ModelSerializer):
    status = ValuedChoiceField(choices=ComponentStatus.choices, required=False)
    finding = PrimaryKeyRelatedField(serializer=FindingSerializer)

    class Meta:
        model = FindingComponent
        fields = ["status", "finding", "data", "pk", "date_created", "date_updated"]
