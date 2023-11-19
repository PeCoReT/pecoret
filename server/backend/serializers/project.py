from rest_framework import serializers
from django.conf import settings
from backend.models.project import Project, TestMethod, ProjectStatus, ScoreChoices
from pecoret.core.serializers import ValuedChoiceField, PrimaryKeyRelatedField
from .pentest_type import PentestTypeSerializer


class ProjectSerializer(serializers.ModelSerializer):
    status = ValuedChoiceField(choices=ProjectStatus.choices)
    test_method = ValuedChoiceField(choices=TestMethod.choices)
    company_name = serializers.SerializerMethodField("get_company_name")
    pentest_types = PrimaryKeyRelatedField(serializer=PentestTypeSerializer, many=True)
    language = ValuedChoiceField(choices=settings.LANGUAGES)
    pinned = serializers.SerializerMethodField()

    def get_company_name(self, obj):
        return obj.company.name

    def get_pinned(self, obj):
        return obj.pinnedproject_set.for_user(self.context["request"].user).exists()

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
            "company_name",
            "pinned",
            "year",
            "pentest_types",
            "require_cvss_score",
            "language",

        ]
        extra_kwargs = {"description": {"required": False}}
