from rest_framework import serializers
from backend.models.membership import Membership, Roles
from pecoret.core.serializers import ValuedChoiceField
from .user import MinimalUserSerializer


class MembershipSerializer(serializers.ModelSerializer):
    role = ValuedChoiceField(choices=Roles.choices)
    user = MinimalUserSerializer()

    class Meta:
        model = Membership
        fields = ["role", "user", "pk", "active_until"]


class MembershipCreateUpdateSerializer(serializers.ModelSerializer):
    role = ValuedChoiceField(choices=Roles.choices)

    class Meta:
        model = Membership
        fields = ["role", "user", "pk", "active_until"]
