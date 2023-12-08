from .base import BaseAssetSerializer
from backend.models import GenericAsset


class GenericAssetSerializer(BaseAssetSerializer):
    class Meta:
        model = GenericAsset
        fields = BaseAssetSerializer.Meta.fields + [
            'name'
        ]
