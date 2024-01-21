from rest_framework import serializers
from backend.models import CompanyInformation
from backend.serializers.user import MinimalUserSerializer
from pecoret.core.serializers import PrimaryKeyRelatedField


class CompanyInformationSerializer(serializers.ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True, serializer=MinimalUserSerializer)
    user_edit = PrimaryKeyRelatedField(read_only=True, serializer=MinimalUserSerializer)

    class Meta:
        model = CompanyInformation
        fields = ["pk", "date_created", "date_updated", "text", "user", "user_edit"]
