from rest_framework.serializers import ModelSerializer

from attack_surface.models import ASN


class ASNSerializer(ModelSerializer):
    class Meta:
        model = ASN
        fields = [
            'date_created', 'date_updated', 'name', 'region_name', 'region',
            'country', 'country_code', 'value', 'city', 'isp',
            'organization', 'timezone', 'zipcode', 'pk'
        ]
