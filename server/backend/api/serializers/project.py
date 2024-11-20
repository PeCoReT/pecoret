from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings
from backend.models.project import Project, TestMethod, ProjectStatus, Visibility
from pecoret.core.serializers import ValuedChoiceField, PrimaryKeyRelatedField
from backend.api.serializers.pentest_type import PentestTypeSerializer
from backend.api.serializers.company import CompanyMinimalSerializer


class ProjectSerializer(serializers.ModelSerializer):
    status = ValuedChoiceField(choices=ProjectStatus.choices)
    test_method = ValuedChoiceField(choices=TestMethod.choices)
    pentest_types = PrimaryKeyRelatedField(serializer=PentestTypeSerializer, many=True)
    language = ValuedChoiceField(choices=settings.LANGUAGES)
    pinned = serializers.SerializerMethodField()
    visibility = ValuedChoiceField(choices=Visibility.choices)
    company = PrimaryKeyRelatedField(serializer=CompanyMinimalSerializer)

    def get_pinned(self, obj) -> bool:
        return obj.pinnedproject_set.for_user(self.context["request"].user).exists()

    def validate_visibility(self, value):
        user = self.context['request'].user
        if not user.is_management_member:
            raise ValidationError({'visibility': 'You cannot change visibility of the project'})
        return value

    class Meta:
        model = Project
        fields = [
            "pk",
            "name",
            "status",
            "date_created",
            "date_updated",
            "company",
            "test_method",
            "start_date",
            "end_date",
            "description",
            "pinned",
            "year",
            "pentest_types",
            "require_cvss_score",
            "language", "visibility"
        ]
        extra_kwargs = {"description": {"required": False}}
