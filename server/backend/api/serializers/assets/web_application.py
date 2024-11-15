from .base import BaseAssetSerializer
from backend.models import WebApplication


class WebApplicationSerializer(BaseAssetSerializer):

    class Meta:
        model = WebApplication
        fields = BaseAssetSerializer.Meta.fields + [
            "base_url", "version", "name"
        ]
