import requests
import logging


class BaseWebhookProvider:

    def __init__(self, webhook):
        self.webhook = webhook
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Webhook',
            'Authorization': f'Bearer {self.webhook.secret}'
        })

    def pre_process_event(self, event):
        """ use this method to pre-process the event before it is being sent"""
        return {'message': event.verb}

    def send(self, event):
        data = self.pre_process_event(event)
        response = self.session.post(self.webhook.url, json=data)
        logging.debug(response.json())
        return response.json()
