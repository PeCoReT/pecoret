from django.conf import settings
from django.utils import timezone
from django.utils.timesince import timesince


class Event:
    def __init__(self, event_name, actor, verb, timestamp=None, action_object=None, target=None, data=None):
        self.name = event_name
        self.actor = actor
        self.verb = verb
        self.action_object = action_object
        self.target = target
        self.timestamp = timestamp
        self.data = data
        if not self.timestamp:
            self.timestamp = timezone.now()

    def _get_action_object_url(self):
        if self.action_object and hasattr(self.action_object, 'get_frontend_url'):
            return self.to_absolute_url(self.action_object.get_frontend_url())
        return None

    def _get_target_url(self):
        if self.target and hasattr(self.target, 'get_frontend_url'):
            return self.to_absolute_url(self.target.get_frontend_url())
        return None

    def to_absolute_url(self, endpoint):
        return f'{settings.SITE_URL}{endpoint}'

    def format_action_object(self):
        """
        give a formatted string representation of an action object in markdown
        Returns: str
        """
        url = self._get_action_object_url()
        if url:
            return f'[{self.action_object}]({url})'
        return f'**{self.action_object}**'

    def format_target(self):
        """
        give a formatted string representation of a target object in markdown
        Returns: str
        """
        target = self._get_target_url()
        if target:
            return f'[{self.target}]({target})'
        return f'**{self.target}**'

    def to_string(self):
        ctx = {
            'target': self.target,
            'actor': self.actor,
            'verb': self.verb,
            'action_object': self.action_object,
            'timesince': timesince(self.timestamp),
        }
        if self.target:
            if self.action_object:
                return '%(actor)s %(verb)s %(action_object)s on %(target)s %(timesince)s ago' % ctx
            return '%(actor)s %(verb)s %(target)s %(timesince)s ago' % ctx
        if self.action_object:
            return '%(actor)s %(verb)s %(action_object)s %(timesince)s ago' % ctx
        return '%(actor)s %(verb)s %(timesince)s ago' % ctx

    def to_markdown_string(self):
        ts = timesince(self.timestamp)
        if self.target:
            if self.action_object:
                return f'{self.actor} {self.verb} {self.format_action_object()} on {self.format_target()} {ts} ago'
            return f'{self.actor} {self.verb} {self.format_target()} {ts} ago'
        if self.action_object:
            return f'{self.actor} {self.verb} {self.format_action_object()} {ts} ago'
        return f'{self.actor} {self.verb} {ts} ago'
