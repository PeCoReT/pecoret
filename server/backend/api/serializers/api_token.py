from rest_framework import serializers
from backend.models.api_token import APIToken, AccessChoices
from pecoret.core.serializers import ValuedChoiceField


class APITokenSerializer(serializers.ModelSerializer):
    scope_all_projects = ValuedChoiceField(AccessChoices.choices)
    scope_user = ValuedChoiceField(AccessChoices.choices)
    scope_companies = ValuedChoiceField(AccessChoices.choices)
    scope_advisories = ValuedChoiceField(AccessChoices.choices)
    scope_attack_surface = ValuedChoiceField(AccessChoices.choices)
    scope_knowledgebase = ValuedChoiceField(AccessChoices.choices)

    class Meta:
        model = APIToken
        fields = [
            "pk", "name", "date_last_used", "date_created",
            "prefix", "scope_advisories", "scope_user",
            "scope_all_projects", "scope_companies",
            "scope_attack_surface", "scope_knowledgebase", "date_expire"
        ]
        read_only_fields = ["date_last_used"]

    def create(self, validated_data):
        token, key = APIToken.objects.create_token(**validated_data)
        token.display_key = key
        return token

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if hasattr(instance, 'display_key'):
            data["token"] = instance.display_key
        return data
