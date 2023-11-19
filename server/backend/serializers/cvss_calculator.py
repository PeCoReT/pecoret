from rest_framework import serializers
from pecoret.core.serializers import ValuedChoiceField
from backend.models.finding import CVSS_40_REGEX, Severity


class CVSS4CalculatorSerializer(serializers.Serializer):
    vector = serializers.RegexField(CVSS_40_REGEX)


class CVSS4CalculatedSerializer(serializers.Serializer):
    severity = ValuedChoiceField(choices=Severity.choices)
    score = serializers.FloatField()
