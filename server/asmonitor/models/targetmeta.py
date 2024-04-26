from django.db import models
from pecoret.core.models import TimestampedModel


class TargetMetaQuerySet(models.QuerySet):
    def for_target(self, target):
        return self.filter(target=target)

    def for_program(self, program):
        return self.filter(target__program=program)


class TargetMeta(TimestampedModel):
    objects = TargetMetaQuerySet.as_manager()
    target = models.ForeignKey('asmonitor.Target', on_delete=models.CASCADE)
    key = models.CharField(max_length=128)
    value = models.TextField()

    class Meta:
        ordering = ['key', 'target']
        unique_together = [
            ('target', 'key')
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # update parents
        self.target.save()
