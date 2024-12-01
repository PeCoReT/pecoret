
from backend.models import CustomFieldAsset
from core.custom_fields.serializers import CustomFieldSerializer


class CustomFieldAssetSerializer(CustomFieldSerializer):
    class Meta:
        model = CustomFieldAsset
        fields = CustomFieldSerializer.Meta.fields
