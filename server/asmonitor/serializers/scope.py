from rest_framework import serializers
from pecoret.core.serializers import ValuedChoiceField
from asmonitor.models.scope import Scope, ScopeTypes


class ScopeSerializer(serializers.ModelSerializer):
    scope_type = ValuedChoiceField(choices=ScopeTypes.choices)

    class Meta:
        model = Scope
        fields = [
            'pk', 'date_updated', 'date_created', 'data', 'scope_type'
        ]
