from rest_framework import serializers

from attack_surface.models.scoping.item import ScopeItem, ScopeItemCategory, ScopeResult
from attack_surface.serializers.scope import ScopeSerializer
from pecoret.core.serializers import ValuedChoiceField, PrimaryKeyRelatedField


class ScopeItemSerializer(serializers.ModelSerializer):
    category = ValuedChoiceField(choices=ScopeItemCategory.choices)
    results_in = ValuedChoiceField(choices=ScopeResult.choices)
    scope = PrimaryKeyRelatedField(serializer=ScopeSerializer)

    class Meta:
        model = ScopeItem
        fields = [
            'pk', 'date_created', 'date_updated', 'value', 'scope',
            'category', 'results_in', 'annotation', 'is_regex'
        ]
