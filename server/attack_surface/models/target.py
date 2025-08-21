import ipaddress
import re
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django_q.tasks import async_task
from djangoql.queryset import DjangoQLQuerySet

from attack_surface.utils import is_subdomain
from core.webhooks.event import Event
from core.webhooks.models import Webhook
from pecoret.core.models import TimestampedModel
from ..utils.djangoql import PecoQLSchema

DOMAIN_REGEX = r"^(?:[a-zA-Z0-9-_]+\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
SUBDOMAIN_REGEX = r"^([a-zA-Z0-9-_]+\.)+[a-zA-Z]{2,}$"


class ScopeChoices(models.IntegerChoices):
    IN_SCOPE = 0, "In Scope"
    UNDEFINED = 1, "Undefined"
    OUT_OF_SCOPE = 2, "Out of Scope"


class DataTypes(models.IntegerChoices):
    IP = 0, "IP"
    # NETWORK = 1, 'Network'
    DOMAIN = 2, "Domain"
    SUBDOMAIN = 3, "Subdomain"


class TargetQuerySet(DjangoQLQuerySet):
    djangoql_schema = PecoQLSchema

    def for_program(self, program):
        return self.filter(program=program)

    def exclude_programs(self, programs):
        return self.exclude(program__in=programs)

    def with_data_type_ip(self):
        return self.filter(data_type=DataTypes.IP)

    def exclude_data_type_ip(self):
        return self.exclude(data_type=DataTypes.IP)

    def filter_unique(self, data, program):
        return self.for_program(program).filter(data=data)

    def with_ip(self, ip):
        return self.filter(resolved_ip=ip)

    def in_scope(self):
        return self.filter(scope=ScopeChoices.IN_SCOPE)

    def get_unique_program_pks(self):
        return (
            self.values_list("program__pk", flat=True)
            .order_by("program__pk")
            .distinct()
        )


class Target(TimestampedModel):
    objects = TargetQuerySet.as_manager()
    data = models.CharField(max_length=512, db_index=True)
    scope = models.PositiveSmallIntegerField(
        choices=ScopeChoices.choices, default=ScopeChoices.UNDEFINED
    )
    program = models.ForeignKey("attack_surface.Program", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    data_type = models.PositiveSmallIntegerField(choices=DataTypes.choices)
    resolved_ip = models.GenericIPAddressField(null=True, blank=True)
    date_asn_last_updated = models.DateTimeField(null=True, blank=True)
    asn = models.ForeignKey(
        "attack_surface.ASN", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["-date_updated", "data"]
        unique_together = [("data", "program")]

    def __str__(self):
        return self.data

    @property
    def display_name(self):
        return self.data

    @property
    def hostnames(self):
        if self.resolved_ip is None:
            return []
        t = Target.objects.with_ip(self.resolved_ip)
        return list(t.values_list("data", flat=True))

    def _calculate_data_type(self):
        try:
            ipaddress.ip_address(self.data)
            return DataTypes.IP
        except ValueError:
            pass
        if re.match(DOMAIN_REGEX, self.data) and not is_subdomain(self.data):
            return DataTypes.DOMAIN
        elif re.match(SUBDOMAIN_REGEX, self.data) and is_subdomain(self.data):
            return DataTypes.SUBDOMAIN
        return

    def save(self, *args, **kwargs):
        if not self.data_type:
            self.data_type = self._calculate_data_type()
        self.full_clean()
        super().save(*args, **kwargs)
        self.program.save()

    def clean(self):
        if not self.data_type:
            raise ValidationError(
                {"data_type": "Data type could not be detected automatically."}
            )
        if self.data_type == DataTypes.IP:
            try:
                ipaddress.ip_address(self.data)
                self.resolved_ip = self.data
            except ValueError:
                raise ValidationError({"data": "Invalid IP"})
        elif self.data_type == DataTypes.DOMAIN:
            if not re.match(DOMAIN_REGEX, self.data) or is_subdomain(self.data):
                raise ValidationError({"data": "Invalid domain"})
        elif self.data_type == DataTypes.SUBDOMAIN:
            if not re.match(SUBDOMAIN_REGEX, self.data) or not is_subdomain(self.data):
                raise ValidationError({"data": "Invalid subdomain"})
        return super().clean()

    @property
    def is_in_scope(self):
        return self.scope == ScopeChoices.IN_SCOPE

    def get_frontend_url(self):
        return f"/#/attack-surface/targets/{self.pk}/"


@receiver(models.signals.post_save, sender=Target)
def webhook_new_target(sender, instance, created, **kwargs):
    if created:
        e = Event(
            "new_target",
            "Scanner",
            "created target",
            action_object=instance,
            target=instance.program,
        )
        for w in Webhook.objects.for_event(e):
            async_task(w.get_provider().send, e)
