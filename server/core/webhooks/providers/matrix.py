from .base import BaseWebhookProvider
from pecoret.core.utils.markdown import markdown2html


class WebhookProvider(BaseWebhookProvider):
    def pre_process_event(self, event):
        data = {
            'msgtype': 'm.text',
            'format': 'org.matrix.custom.html',
            'body': event.to_markdown_string(),
            'formatted_body': markdown2html(event.to_markdown_string(), limited=True)
        }
        return data
