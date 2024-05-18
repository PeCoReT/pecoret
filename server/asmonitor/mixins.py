from django.core.validators import ValidationError
from rest_framework.exceptions import NotFound

from asmonitor.models.target import Target


class TargetRelatedMixin:
    def get_target(self, validation_error=False):
        try:
            target = Target.objects.get(pk=self.kwargs.get('target'), program__pk=self.kwargs.get('program'))
        except Target.DoesNotExist:
            if validation_error is True:
                raise ValidationError({'target': 'Invalid target'})
            raise NotFound()
        return target
