from django.core.validators import RegexValidator
from rest_framework import serializers


class ScannerEventSerializer(serializers.Serializer):
    event_type = serializers.CharField(
        validators=[RegexValidator(regex=r"^[a-z0-9-.:]+$")]
    )
    payload = serializers.DictField(required=False, allow_null=True)
    raw_line = serializers.CharField(required=False, allow_null=True)
    bulk = serializers.ListField(
        child=serializers.DictField(), required=False, allow_null=True
    )
    output = serializers.CharField(required=False, allow_null=True)
    errors = serializers.CharField(required=False, allow_null=True)
