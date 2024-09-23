from rest_framework import serializers

from attack_surface.models.scanner import Scanner
from attack_surface.serializers.scanning.scan_type import ScanTypeSerializer
from pecoret.core.serializers import PrimaryKeyRelatedField


class ScannerSerializer(serializers.ModelSerializer):
    scan_types = PrimaryKeyRelatedField(many=True, serializer=ScanTypeSerializer)

    class Meta:
        model = Scanner
        fields = ['pk', 'last_seen', 'name', 'scan_types']


class ScannerCreateSerializer(ScannerSerializer):
    class Meta:
        model = Scanner
        # show token only when created
        fields = ScannerSerializer.Meta.fields + ['token']


class ScannerLastSeenSerializer(serializers.ModelSerializer):
    """ used by the scanner to set status and last seen """
    class Meta:
        model = Scanner
        fields = ['last_seen']
        read_only_fields = ['last_seen']
