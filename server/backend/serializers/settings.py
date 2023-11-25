from rest_framework import serializers
from backend.models.settings import Settings


class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        exclude = ['id']
