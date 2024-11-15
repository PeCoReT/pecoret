from rest_framework import serializers
from backend.models import CompanyInformation
from backend.api.serializers.user import MinimalUserSerializer
from pecoret.core.serializers import PrimaryKeyRelatedField
from pecoret.core.utils.markdown import MarkdownHTMLRenderer


class CompanyInformationSerializer(serializers.ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True, serializer=MinimalUserSerializer)
    user_edit = PrimaryKeyRelatedField(read_only=True, serializer=MinimalUserSerializer)
    text_md = serializers.SerializerMethodField()

    class Meta:
        model = CompanyInformation
        fields = ["pk", "date_created", "date_updated", "text", "user", "user_edit", "text_md"]

    def get_text_md(self, value):
        renderer = MarkdownHTMLRenderer(limited=True)
        return renderer.render(value.text)
