import warnings

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings

from pecoret.core.models import TimestampedModel
from pecoret.core.validators.cvss import cvss_regex_validator
from pecoret.reporting.utils import get_report_template_choices
from advisories.models.advisory_timeline import AdvisoryTimeline
from backend.models.finding import Severity
from backend.models.technology import Technology


def create_advisory_id():
    year = timezone.now().year
    qs = Advisory.objects.filter(
        date_created__date__year=year, advisory_id__isnull=False
    ).order_by("advisory_id")
    # first advisory this year
    if not qs.exists():
        return f"{year}-0001"
    last_id = qs.last().advisory_id.split("-")[-1]
    length = len(str(last_id))
    if length < 4:
        formatter = "%04d"
    else:
        formatter = "%0{len}d".format(len=length)
    new_pk = formatter % int(int(last_id) + 1)
    return f"{year}-{new_pk}"


class AdvisoryStatusChoices(models.IntegerChoices):
    NOT_DISCLOSED = 1, "Not Disclosed"
    DISCLOSED = 2, "Disclosed"


class VulnerabilityStatusChoices(models.IntegerChoices):
    UNFIXED = 1, "Unfixed"
    FIXED = 2, "Fixed"
    WONT_FIX = 3, "Won't Fix"


class AdvisoryQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.all()

    def for_share_token(self, token):
        return self.filter(sharetoken__token=token)

    def disclosed(self):
        return self.filter(status=AdvisoryStatusChoices.DISCLOSED)

    def not_disclosed(self):
        return self.filter(status=AdvisoryStatusChoices.NOT_DISCLOSED)

    def unfixed(self):
        return self.filter(status=VulnerabilityStatusChoices.UNFIXED)

    def fixed(self):
        return self.filter(status=VulnerabilityStatusChoices.FIXED)

    def wont_fix(self):
        return self.filter(status=VulnerabilityStatusChoices.WONT_FIX)

    def count_by_user(self):
        return (
            self.values("user__username")
            .annotate(count=models.Count("pk"))
            .order_by("-count")
        )


class AdvisoryManager(models.Manager):
    def create_from_data(self, **data):
        data["date_planned_disclosure"] = timezone.now() + timezone.timedelta(
            days=settings.ADVISORY_DISCLOSURE_TIMEDELTA
        )
        cwes = data.pop("cwes", None)
        advisory = self.create(**data)
        if cwes:
            advisory.cwes.set(cwes)
        return advisory

    def create_from_finding(self, finding, **data):
        data["date_planned_disclosure"] = timezone.now() + timezone.timedelta(
            days=settings.ADVISORY_DISCLOSURE_TIMEDELTA
        )
        data["severity"] = finding.severity
        data["user"] = finding.user
        data["proof_text"] = finding.proof_text
        data["title"] = finding.name
        data["report_template"] = list(settings.REPORT_TEMPLATES.keys())[0]
        data["recommendation"] = finding.vulnerability.recommendation
        data["technology"] = Technology.objects.get(pk=data["technology"])
        advisory = self.create(**data)
        if finding.recommendation:
            advisory.recommendation = finding.recommendation
        else:
            advisory.recommendation = finding.vulnerability.recommendation
        return advisory


class Advisory(TimestampedModel):
    objects = AdvisoryManager.from_queryset(AdvisoryQuerySet)()
    id = models.BigAutoField(primary_key=True)
    advisory_id = models.CharField(max_length=64, default=create_advisory_id)
    user = models.ForeignKey("backend.User", on_delete=models.PROTECT)
    date_planned_disclosure = models.DateField()
    date_disclosure = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=128)
    affected_versions = models.CharField(max_length=128)
    fixed_version = models.CharField(max_length=128, blank=True, null=True)
    cwes = models.ManyToManyField("backend.CWE")
    severity = models.PositiveSmallIntegerField(choices=Severity.choices)
    cve_id = models.CharField(max_length=20, null=True, blank=True)
    technology = models.ForeignKey("backend.Technology", on_delete=models.PROTECT)
    description = models.TextField(null=True, blank=True)
    recommendation = models.TextField(null=True, blank=True)
    labels = models.ManyToManyField("advisories.Label", blank=True)
    custom_report_title = models.CharField(max_length=255, null=True, blank=True)
    hide_advisory_id_in_report = models.BooleanField(default=False)
    proof_text = models.TextField(blank=True, default="")
    is_draft = models.BooleanField(default=True)
    report_template = models.CharField(
        max_length=128, choices=get_report_template_choices
    )
    status = models.PositiveSmallIntegerField(
        choices=AdvisoryStatusChoices.choices,
        default=AdvisoryStatusChoices.NOT_DISCLOSED,
    )
    vulnerability_status = models.PositiveSmallIntegerField(
        choices=VulnerabilityStatusChoices.choices,
        default=VulnerabilityStatusChoices.UNFIXED,
    )
    # overwrites the default "user" display name in the research section of the PDF
    researchers = models.CharField(max_length=512, null=True, blank=True)
    image_files = GenericRelation(to="storage.ImageFile")
    cvss_vector = models.CharField(
        max_length=255, null=True, blank=True, validators=[cvss_regex_validator]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.advisory_id

    def get_researchers(self):
        if self.researchers:
            return self.researchers
        return self.user.report_display_name

    def get_advisory_id_display(self):
        prefix = settings.ADVISORY_ID_PREFIX
        return f"{prefix}{self.advisory_id}"

    @property
    def vendor_url(self):
        warnings.warn("Use `technology.homepage` field instead", DeprecationWarning)
        return self.technology.homepage

    @property
    def vendor_name(self):
        warnings.warn("Use `technology.vendor` field instead", DeprecationWarning)
        return self.technology.vendor

    @property
    def product(self):
        warnings.warn("Use `technology.name` field instead", DeprecationWarning)
        return self.technology.name

    class Meta:
        ordering = ["-advisory_id", "date_updated"]
        db_table = "backend_advisory"


@receiver(models.signals.post_save, sender=Advisory)
def on_advisory_create(sender, instance, created, **kwargs):
    if created:
        AdvisoryTimeline.objects.create(
            date=timezone.now(), text="Advisory created", advisory=instance
        )
