from rest_framework import serializers
from backend.models import Account


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [
            "pk",
            "date_created",
            "date_updated",
            "role",
            "username",
            "password",
            "accessible",
            "compromised",
            "description"
        ]
