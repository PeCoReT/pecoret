from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class ObjectLockQuerySet(models.QuerySet):
    def with_object(self, obj_name, obj_id):
        return self.filter(**{obj_name: obj_id})


class ObjectLock(models.Model):
    object_choices = models.Q(app_label='backend', model='projectnote')

    objects = ObjectLockQuerySet.as_manager()
    user = models.ForeignKey('backend.User', on_delete=models.CASCADE)
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=object_choices)
    object_id = models.PositiveSmallIntegerField()
    locked_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ['-last_seen']
        indexes = [
            models.Index(fields=['content_type', 'object_id'])
        ]
        unique_together = [
            ('content_type', 'object_id')
        ]
