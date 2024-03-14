from django.db import models
from django.core.validators import RegexValidator
from pecoret.core.models import PeCoReTBaseModel, TimestampedModel


class Tag(PeCoReTBaseModel, TimestampedModel):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=7, validators=[
        RegexValidator(regex=r'#([a-fA-F\d]{6}|[a-fA-F\d]{3})')
    ])

    def __str__(self):
        return self.name

    @property
    def color_rgb(self):
        value = self.color.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    class Meta:
        ordering = ["name"]
