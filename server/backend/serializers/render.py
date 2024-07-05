from rest_framework import serializers
from pecoret.core.utils.markdown import md_to_clean_html


class RenderMarkdownSerializer(serializers.Serializer):
    markdown = serializers.CharField(write_only=True)
    html = serializers.SerializerMethodField(read_only=True)

    def get_html(self, obj):
        return md_to_clean_html(obj['markdown'])
