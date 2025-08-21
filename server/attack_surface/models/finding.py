from django.db import models
from django.db.models.fields import validators
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from backend.models.finding import CVSS_31_REGEX
from backend.models.vulnerability import Severity
from pecoret.core.models import TimestampedModel, CASCADE_USER_TO_GHOST
from pecoret.core.models.locked_model import LockedModel, AbstractLockedModel


class ProgressStatus(models.IntegerChoices):
    DRAFT = 0, "Draft"
    REVIEW_REQUIRED = 1, "Review Required"
    FINAL = 2, "Final"


def create_finding_id():
    year = timezone.now().year
    month = timezone.now().month
    amount = Finding.objects.filter(
        date_created__date__year=year, date_created__date__month=month
    ).count()
    return f"{year}{month}{amount+1}"


class Finding(AbstractLockedModel, TimestampedModel):
    finding_id = models.CharField(
        max_length=128, default=create_finding_id, unique=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    recommendation = models.TextField(null=True, blank=True)
    created_by_user = models.ForeignKey(
        "backend.User", on_delete=CASCADE_USER_TO_GHOST, related_name="created_findings"
    )
    edited_by_user = models.ForeignKey(
        "backend.User",
        on_delete=models.SET_NULL,
        related_name="edited_findings",
        null=True,
        blank=True,
    )

    severity = models.PositiveSmallIntegerField(
        choices=Severity.choices, null=True, blank=True
    )

    cwe_ids = models.ManyToManyField(
        "backend.CWE", blank=True, related_name="as_finding_set"
    )
    cvss_score = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validators.RegexValidator(regex=CVSS_31_REGEX)],
    )
    internal_notes = models.TextField(
        blank=True,
        null=True,
        help_text="Internal Notes should not be exposed in custom templates",
    )
    exploitation_details = models.TextField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        choices=ProgressStatus.choices, default=ProgressStatus.DRAFT
    )
    program = models.ForeignKey("attack_surface.Program", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def _get_required_fields(self):
        return [
            "cvss_score",
            "severity",
            "description",
            "recommendation",
            "exploitation_details",
            "cwe_ids",
        ]

    def clean(self):
        """ensure that finding cannot leave draft status unless required fields are set"""
        if self.status == ProgressStatus.DRAFT:
            return
        required_fields = self._get_required_fields()
        missing_fields = [
            field for field in required_fields if not getattr(self, field)
        ]
        if missing_fields:
            raise ValidationError(
                {
                    field: f'{field.replace("_", " ").capitalize()} is required for this status.'
                    for field in missing_fields
                }
            )
        if self.findingcomponent_set.count() < 1:
            raise ValidationError(
                {"components": "at least one affected component is required"}
            )

    class Meta:
        ordering = ["-date_created", "title"]
