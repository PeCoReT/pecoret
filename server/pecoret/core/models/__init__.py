from django.db import models
from backend.models import User


class PeCoReTBaseModel(models.Model):
    """a base model that can be used to always perform full_clean on save
    """
    class Meta:
        abstract = True

    def pre_save(self):
        pass

    def post_save(self):
        pass

    def save(self, *args, **kwargs):
        """always do a `full_clean` on save
        """
        self.pre_save()
        self.full_clean(validate_unique=False)
        super().save(*args, **kwargs)
        self.post_save()


class TimestampedModel(models.Model):
    """model which just tracks dates for udpate and create
    """
    date_created = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-date_created", "-date_updated"]


def CASCADE_USER_TO_GHOST(collector, field, sub_objs, using):
    for obj in sub_objs:
        if obj.user:
            obj.user = User.objects.get(username="Ghost")
    models.CASCADE(collector, field, sub_objs, using)
