from rest_framework import serializers
from backend.models.project_contact import ProjectContact
from pecoret.core.serializers import CompanyScopedPrimaryKeyRelatedField
from .company_contact import CompanyContactSerializer


class ProjectContactSerializer(serializers.ModelSerializer):
    contact = CompanyScopedPrimaryKeyRelatedField(serializer=CompanyContactSerializer)

    class Meta:
        model = ProjectContact
        fields = ["pk", "date_created", "date_updated", "contact"]
