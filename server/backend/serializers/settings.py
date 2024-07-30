import copy

from rest_framework import serializers
from django.core.exceptions import ValidationError
from extra_settings.models import Setting

FIELD_MAPPINGS = {
    Setting.TYPE_EMAIL: serializers.EmailField
}


class SettingSerializer(serializers.ModelSerializer):
    setting_value = serializers.CharField(write_only=True)
    value = serializers.CharField(read_only=True)
    value_type = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)

    class Meta:
        model = Setting
        fields = ['pk', 'name', 'value', 'setting_value', 'value_type', 'description']

    def to_internal_value(self, data):
        try:
            self.instance.value = data['setting_value']
            # extra_settings package does not validate value on property setter. do it manually here!
            self.instance.full_clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        except Exception as e:
            print(e)
            return None
        return data

