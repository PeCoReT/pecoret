from rest_framework import serializers


class LanguageSerializer(serializers.Serializer):
    language = serializers.CharField()
    code = serializers.CharField()
