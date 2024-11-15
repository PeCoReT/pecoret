from rest_framework import serializers
from backend.models import CWE


class CWESerializer(serializers.ModelSerializer):
    class Meta:
        model = CWE
        fields = [
            "cwe_id", "name", "description", "pk"
        ]


class CWEMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CWE
        fields = ["cwe_id", "pk", "name"]
