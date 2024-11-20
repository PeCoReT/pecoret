from rest_framework import serializers
from backend.models.company_contact import CompanyContact


class CompanyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyContact
        fields = [
            "pk",
            "first_name",
            "last_name",
            "phone",
            "email",
            "role",
            "pgp_public_key",
        ]
