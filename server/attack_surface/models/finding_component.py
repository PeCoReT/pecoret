from django.db import models

from pecoret.core.validators.schemes import generic_url_validator
from pecoret.core.models import TimestampedModel


class ComponentStatus(models.IntegerChoices):
    VULNERABLE = 0, "Vulnerable"
    FIXED = 1, "Fixed"
    WONT_FIX = 2, "Wont Fix"


class FindingComponent(TimestampedModel):
    finding = models.ForeignKey("attack_surface.Finding", on_delete=models.CASCADE)
    data = models.CharField(max_length=512, validators=[generic_url_validator])
    status = models.PositiveSmallIntegerField(
        choices=ComponentStatus.choices, default=ComponentStatus.VULNERABLE
    )

    class Meta:
        unique_together = (("finding", "data"),)
        ordering = ["-date_updated"]
