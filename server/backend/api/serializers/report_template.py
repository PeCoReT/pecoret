from rest_framework import serializers


class ReportTemplateSerializer(serializers.Serializer):
    name = serializers.CharField()
