from rest_framework import serializers
from pecoret.core.utils.markdown import markdown2html


class RenderMarkdownSerializer(serializers.Serializer):
    markdown = serializers.CharField(write_only=True, allow_blank=True)
    html = serializers.SerializerMethodField(read_only=True)

    def get_html(self, obj) -> str:
        limited = True
        if self.context.get('request') and not self.context['request'].user.is_markdown_limited():
            limited = False
        return markdown2html(obj['markdown'], limited=limited)
