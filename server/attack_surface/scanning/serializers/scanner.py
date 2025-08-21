from rest_framework import serializers

from attack_surface.models.scanner import Scanner


class ScannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scanner
        fields = ['pk', 'last_seen', 'name']


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
