from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.conf import settings
from backend.models.project import Project, TestMethod, ProjectStatus, Visibility
from pecoret.core.serializers import ValuedChoiceField, PrimaryKeyRelatedField
from pecoret.core.utils.markdown import markdown2html
from backend.api.serializers.pentest_type import PentestTypeSerializer
from backend.api.serializers.company import CompanyMinimalSerializer


class ProjectSerializer(serializers.ModelSerializer):
    status = ValuedChoiceField(choices=ProjectStatus.choices)
    test_method = ValuedChoiceField(choices=TestMethod.choices)
    project_types = PrimaryKeyRelatedField(serializer=PentestTypeSerializer, many=True)
    language = ValuedChoiceField(choices=settings.LANGUAGES)
    pinned = serializers.SerializerMethodField()
    visibility = ValuedChoiceField(choices=Visibility.choices)
    company = PrimaryKeyRelatedField(serializer=CompanyMinimalSerializer)
    description_md = serializers.SerializerMethodField()

    def get_pinned(self, obj) -> bool:
        return obj.pinnedproject_set.for_user(self.context["request"].user).exists()

    def get_description_md(self, obj):
        return markdown2html(obj.description)

    def validate_visibility(self, value):
        user = self.context["request"].user
        if not user.is_management_member and not user.is_superuser:
            raise ValidationError(
                {"visibility": "You cannot change visibility of the project"}
            )
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
            "project_types",
            "require_cvss_score",
            "language",
            "visibility",
            "description_md",
        ]
        extra_kwargs = {"description": {"required": False}}
