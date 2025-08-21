from rest_framework import serializers
from core.webhooks.models.webhook import Webhook


class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webhook
        fields = [
            'pk', 'date_created', 'date_updated', 'secret',
            'url', 'additional_data', 'provider',
            # events
            'event_new_target',
            'event_critical_scan_finding'
        ]
