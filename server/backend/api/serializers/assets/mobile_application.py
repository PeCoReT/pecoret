from pecoret.core.serializers import ValuedChoiceField
from .base import BaseAssetSerializer
from backend.models.assets.mobile_application import MobileApplication, OperatingSystem


class MobileApplicationSerializer(BaseAssetSerializer):
    os = ValuedChoiceField(choices=OperatingSystem.choices)

    class Meta:
        model = MobileApplication
        fields = BaseAssetSerializer.Meta.fields + [
            "os", "name", "certificate_pinning", "version"
        ]
