from pecoret.core.serializers import ValuedChoiceField
from .base import BaseAssetSerializer
from backend.models.assets.thick_client import ThickClient, OperatingSystem, DecompileAllowedChoices


class ThickClientSerializer(BaseAssetSerializer):
    os = ValuedChoiceField(choices=OperatingSystem.choices)
    decompile_allowed = ValuedChoiceField(choices=DecompileAllowedChoices.choices)

    class Meta:
        model = ThickClient
        fields = BaseAssetSerializer.Meta.fields + [
            "os", "name", "programming_language", "decompile_allowed", "version"
        ]
