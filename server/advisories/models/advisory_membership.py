from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from pecoret.core.models import PeCoReTBaseModel, TimestampedModel


class Roles(models.IntegerChoices):
    CREATOR = 0, "Creator"
    READ_ONLY = 1, "Read Only"
    VENDOR = 2, "Vendor"


class AdvisoryMembershipQuerySet(models.QuerySet):
    def for_advisory(self, advisory):
        return self.filter(advisory=advisory)


class AdvisoryMembership(TimestampedModel, PeCoReTBaseModel):
    objects = AdvisoryMembershipQuerySet.as_manager()
    user = models.ForeignKey('backend.User', on_delete=models.CASCADE)
    advisory = models.ForeignKey('advisories.Advisory', on_delete=models.CASCADE)
    active_until = models.DateTimeField(blank=True, default=None, null=True)
    role = models.PositiveSmallIntegerField(choices=Roles.choices, default=Roles.READ_ONLY)

    class Meta:
        ordering = ["-date_created"]
        unique_together = [
            ("user", "advisory")
        ]
        db_table = 'backend_advisorymembership'

    def clean(self):
        try:
            instance = AdvisoryMembership.objects.get(pk=self.pk)
            if instance.user_id != self.user_id:
                raise ValidationError(
                    {"user": "Membership user cannot be changed after creation."}
                )
        except ObjectDoesNotExist:
            pass
        return super().clean()

    @property
    def active(self):
        if not self.active_until:
            return True
        if self.active_until > timezone.now():
            return True
        return False

    def __str__(self):
        return f"{self.user} ({self.get_role_display()}) for {self.advisory}"
