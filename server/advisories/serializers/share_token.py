from rest_framework import serializers

from advisories.models.share_token import ShareToken


class ShareTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareToken
        fields = ['token', 'date_created', 'date_updated', 'date_expire', 'url', 'name', 'pk']
        read_only_fields = ['token']
