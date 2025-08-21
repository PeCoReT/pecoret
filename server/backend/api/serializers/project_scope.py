from rest_framework import serializers
from pecoret.core.serializers import ValuedChoiceField
from backend.models.project_scope import ProjectScope, ScopePermission


class ProjectScopeSerializer(serializers.ModelSerializer):
    permission = ValuedChoiceField(choices=ScopePermission.choices)

    class Meta:
        model = ProjectScope
        fields = ["pk", "permission", "details"]
