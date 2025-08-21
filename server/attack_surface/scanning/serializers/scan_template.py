from rest_framework import serializers

from attack_surface.scanning.models import ScanTemplate
from attack_surface.scanning.models.scan_template import PriorityChoices
from pecoret.core.serializers import ValuedChoiceField


class MinimalScanTemplateSerializer(serializers.ModelSerializer):
    priority = ValuedChoiceField(choices=PriorityChoices.choices)

    class Meta:
        model = ScanTemplate
        fields = [
            'pk', 'name', 'scan_type', 'priority', 'cooldown',
            'rate_limit', 'batch_threshold', 'trickle_delay',
            'is_discovery_scan', 'enabled', 'description',
            'conditions', 'input_type'
        ]


class ScanTemplateSerializer(MinimalScanTemplateSerializer):
    class Meta:
        model = ScanTemplate
        fields = MinimalScanTemplateSerializer.Meta.fields + ['scanner_config']
