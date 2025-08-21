from django.db import models
from rest_framework.exceptions import ValidationError

from pecoret.core.models import TimestampedModel


class ExclusionRuleQuerySet(models.QuerySet):
    def with_scan_template(self, scan_template):
        return self.filter(scan_templates=scan_template)

    def distinct_item_pks(self, field):
        filters = {
            f'{field}__isnull': False,
        }
        return self.filter(**filters).values_list(field, flat=True).distinct()


class ExclusionRule(TimestampedModel):
    objects = ExclusionRuleQuerySet.as_manager()
    # Relationships to Program, Target, Service, or URL
    program = models.ForeignKey('attack_surface.Program', on_delete=models.CASCADE, null=True, blank=True,
                                help_text="excluding a program, will automatically exclude all related items")
    target = models.ForeignKey('attack_surface.Target', on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey('attack_surface.Service', on_delete=models.CASCADE, null=True, blank=True)
    url = models.ForeignKey('attack_surface.URL', on_delete=models.CASCADE, null=True, blank=True)

    # Many-to-Many relationship for ScanTemplates
    scan_templates = models.ManyToManyField('ScanTemplate', blank=True)

    exclusion_reason = models.TextField(blank=True, null=True)  # Reason for exclusion (e.g., "Maintenance window")

    class Meta:
        unique_together = ['program', 'target', 'service', 'url']
        verbose_name_plural = 'Exclusion Rules'

    def __str__(self):
        return f"Exclusion Rule for {', '.join([str(template) for template in self.scan_templates.all()])}"

    def clean(self):
        fields = [self.program, self.target, self.service, self.url]
        non_null_fields = [f for f in fields if f is not None]
        if len(non_null_fields) != 1:
            raise ValidationError({"fk": "Exactly one of 'program', 'target', 'service', or 'url' must be set."})
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
