from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.utils import timezone
from pecoret.core.models import TimestampedModel, PeCoReTBaseModel


class Roles(models.IntegerChoices):
    PROJECT_LEADER = 0, "Project Leader"
    CONTRIBUTOR = 1, "Contributor"
    READ_ONLY = 2, "Read Only"
    CUSTOMER = 3, "Customer"
    OWNER = 4, "Owner"


class MembershipManager(models.Manager):
    def create(self, **kwargs):
        membership = Membership(**kwargs)
        membership.save(force_insert=True)
        return membership


class MembershipQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(project=project)

    def for_user(self, user):
        return self.filter(user=user)

    def for_roles(self, roles):
        return self.filter(role__in=roles)

    def for_report(self):
        return self.filter(display_in_report=True)

    def is_active(self):
        return self.filter(models.Q(active_until__isnull=True) | models.Q(active_until__gte=timezone.now()))


class Membership(TimestampedModel, PeCoReTBaseModel):
    objects = MembershipManager.from_queryset(MembershipQuerySet)()
    user = models.ForeignKey('backend.User', on_delete=models.PROTECT)
    project = models.ForeignKey('backend.Project', on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=Roles.choices, default=Roles.CONTRIBUTOR)
    active_until = models.DateTimeField(blank=True, default=None, null=True)
    display_in_report = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date_created"]
        unique_together = [
            ("user", "project")
        ]

    def __str__(self):
        return f"{Roles(self.role).name} ({self.user} in {self.project})"

    def clean(self):
        try:
            instance = Membership.objects.get(pk=self.pk)
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
