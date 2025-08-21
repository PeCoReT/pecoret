from django.db import models
from rest_framework.exceptions import ValidationError

from pecoret.core.models import TimestampedModel


class ScopeItemCategory(models.IntegerChoices):
    DOMAIN = 0, 'Domain'
    KEYWORD = 1, 'Keyword'
    MAIL = 2, 'Mail'


class ScopeResult(models.IntegerChoices):
    INCLUDE = 0, 'Include'
    EXCLUDE = 1, 'Exclude'


class ScopeItemQuerySet(models.QuerySet):
    def for_program(self, program):
        return self.filter(scope__program=program)

    def for_scope(self, scope):
        return self.filter(scope=scope)

    def domains(self):
        return self.filter(category=ScopeItemCategory.DOMAIN)

    def no_domains(self):
        return self.exclude(category=ScopeItemCategory.DOMAIN)

    def keywords(self):
        return self.filter(category=ScopeItemCategory.KEYWORD)

    def no_keywords(self):
        return self.exclude(category=ScopeItemCategory.KEYWORD)

    def excludes(self):
        return self.filter(results_in=ScopeResult.EXCLUDE)

    def  includes(self):
        return self.filter(results_in=ScopeResult.INCLUDE)


class ScopeItem(TimestampedModel):
    objects = ScopeItemQuerySet.as_manager()
    scope = models.ForeignKey('attack_surface.Scope', on_delete=models.CASCADE)
    value = models.TextField()
    category = models.PositiveSmallIntegerField(choices=ScopeItemCategory)
    results_in = models.PositiveSmallIntegerField(choices=ScopeResult)
    annotation = models.CharField(max_length=255, blank=True, null=True)
    is_regex = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.scope} - {self.value}'

    class Meta:
        unique_together = ('scope', 'value')

    def clean(self):
        if self.is_regex and self.category == ScopeItemCategory.KEYWORD:
            raise ValidationError({'is_regex': 'Keyword cannot be a regex.'})
        # Enforce: No two programs can have the same value in scope
        if not self.pk:  # Only apply on create
            existing = ScopeItem.objects.filter(value=self.value).exclude(scope__program=self.scope.program)
            if existing.exists():
                raise ValidationError({'value': 'This value is already in scope for another program.'})
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
