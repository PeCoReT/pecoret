from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class LockedModel(models.Model):
    class Meta:
        abstract = True

    @property
    def object_lock_instance(self):
        if not self.object_lock:
            return None
        return self.object_lock.first()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_lock()

    def validate_lock(self, current_user):
        if not self.object_lock_instance:
            return
        if current_user.pk == self.object_lock_instance.user.pk:
            return
        raise ValidationError({'self': 'object is locked'})

    def check_lock(self):
        if self.object_lock_instance:
            delta = timezone.now() - self.object_lock_instance.last_seen
            if delta > timezone.timedelta(seconds=90):
                self.object_lock_instance.delete()
