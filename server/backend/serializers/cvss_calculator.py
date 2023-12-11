from rest_framework import serializers
from pecoret.core.serializers import ValuedChoiceField
from backend.models.finding import CVSS_40_REGEX, Severity, CVSS_31_REGEX


class CVSS4CalculatorSerializer(serializers.Serializer):
    vector = serializers.RegexField(CVSS_40_REGEX)


class CVSS4CalculatedSerializer(serializers.Serializer):
    severity = ValuedChoiceField(choices=Severity.choices)
    score = serializers.FloatField()


class CVSS31CalculatorSerializer(serializers.Serializer):
    vector = serializers.RegexField(CVSS_31_REGEX)


class CVSS31CalculatedSerializer(serializers.Serializer):
    severity = ValuedChoiceField(choices=Severity.choices)
    score = serializers.FloatField()
