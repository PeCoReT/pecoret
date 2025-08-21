from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
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
        raise ValidationError({"self": "object is locked"})

    def check_lock(self):
        if self.object_lock_instance:
            delta = timezone.now() - self.object_lock_instance.last_seen
            if delta > timezone.timedelta(seconds=90):
                self.object_lock_instance.delete()


class AbstractLockedModelQuerySet(models.QuerySet):
    def locked(self):
        # get all locked objects
        return self.filter(locked_by__null=False)

    def unlocked(self):
        return self.filter(locked_by__null=True)


class AbstractLockedModel(models.Model):
    """
    abstract model for a model that can be locked by a user
    """

    objects = AbstractLockedModelQuerySet.as_manager()
    # unlock model when user is deleted
    locked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="locked_items",
    )
    locked_date = models.DateTimeField(blank=True, null=True)

    @property
    def is_locked(self):
        if self.locked_by:
            return True
        return False

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True
