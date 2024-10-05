from django.core.exceptions import ValidationError
from rest_framework import serializers

from attack_surface.models import Scan
from attack_surface.models.scan import ScanStatus
from attack_surface.serializers.scanning.scan_object import ScanObjectSerializer
from attack_surface.serializers.scanning.scan_type import ScanTypeSerializer
from pecoret.core.serializers import ValuedChoiceField, PrimaryKeyRelatedField


class MinimalScanSerializer(serializers.ModelSerializer):
    scan_objects = ScanObjectSerializer(many=True, source='scanobject_set')
    scan_type = PrimaryKeyRelatedField(serializer=ScanTypeSerializer)

    class Meta:
        fields = [
            'pk', 'scan_type', 'scan_objects', 'name', 'output', 'started_at', 'finished_at',
        ]
        read_only_fields = ['output', 'started_at', 'finished_at']
        model = Scan

    def validate_scan_objects(self, value):
        if len(value) < 1:
            raise ValidationError({'scan_objects': 'at least one scan object is required'})
        return value

    def validate_scan_type(self, value):
        if self.context['request'].user.is_authenticated:
            # it's a user
            if value.can_run_manually:
                return value
            raise ValidationError({'scan_type': 'This scan type cannot be run manually'})
        # from scanner
        return value


    def create(self, validated_data):
        obj_data = validated_data.pop('scanobject_set')
        # Create the Scan object first
        scan = Scan.objects.create(**validated_data)
        # Create each ScanObject, validating each one
        for target_data in obj_data:
            target_data['scan'] = scan
            serializer = ScanObjectSerializer(data=target_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(scan=scan)
        return scan


class ScanUpdateSerializer(MinimalScanSerializer):
    scan_objects = ScanObjectSerializer(many=True, source='scanobject_set', read_only=True)
    scan_type = PrimaryKeyRelatedField(serializer=ScanTypeSerializer, read_only=True)

    class Meta:
        model = Scan
        fields = ['pk', 'name', 'started_at', 'finished_at', 'scan_type']
        extra_kwargs = {
            'scan_type': {'read_only': True},
        }
        read_only_fields = ['output', 'started_at', 'finished_at']


class ScannerScanUpdateSerializer(serializers.ModelSerializer):
    status = ValuedChoiceField(choices=ScanStatus.choices)

    class Meta:
        model = Scan
        fields = ['name', 'started_at', 'finished_at', 'output', 'pk', 'status']


class ScanSerializer(MinimalScanSerializer):
    status = ValuedChoiceField(choices=ScanStatus.choices, read_only=True)

    class Meta:
        model = Scan
        fields = MinimalScanSerializer.Meta.fields + ['status']
        read_only_fields = ['output']
