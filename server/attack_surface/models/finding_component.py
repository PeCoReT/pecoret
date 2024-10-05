from django.db import models

from pecoret.core.models import TimestampedModel


class ComponentStatus(models.IntegerChoices):
    VULNERABLE = 0, 'Vulnerable'
    FIXED = 1, 'Fixed'
    WONT_FIX = 2, 'Wont Fix'


class FindingComponent(TimestampedModel):
    finding = models.ForeignKey('attack_surface.Finding', on_delete=models.CASCADE)
    component = models.ForeignKey('attack_surface.Service', on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=ComponentStatus.choices, default=ComponentStatus.VULNERABLE)

    class Meta:
        unique_together = (('finding', 'component'),)
        ordering = ['-date_updated']
