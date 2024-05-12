from django.db import models
from pecoret.core.models import TimestampedModel


class TargetMetaQuerySet(models.QuerySet):
    def for_host(self, host):
        return self.filter(host=host)

    def for_program(self, program):
        return self.filter(target__program=program)


class TargetMeta(TimestampedModel):
    objects = TargetMetaQuerySet.as_manager()
    host = models.ForeignKey('asmonitor.Host', on_delete=models.CASCADE)
    key = models.CharField(max_length=128)
    value = models.TextField()

    class Meta:
        ordering = ['key', 'host']
        unique_together = [
            ('host', 'key')
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # update parents
        self.host.save()
