import copy
import re

import cvss
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext as _
from django_q.tasks import async_task

from backend.tasks import mail
from backend.utils import cvss4
from .cwe import CWE
from .finding_timeline import FindingTimeline
from .vulnerability import Severity, ProjectVulnerability

CVSS_40_REGEX = (r'CVSS:4\.0\/AV:[N|A|L|P]\/AC:[L|H]\/AT:[N|P]\/PR:[N|L|H]\/UI:[N|P|A]\/VC:[H|L|N]\/'
                 r'VI:[H|L|N]\/VA:[H|L|N]\/SC:[H|L|N]\/SI:[H|L|N]\/SA:[H|L|N]')

CVSS_31_REGEX = r'CVSS:3\.1/AV:[N|A|L|P]/AC:[L|H]/PR:[N|L|H]/UI:[N|R]/S:[C|U]/C:[N|L|H]/I:[N|L|H]/A:[N|L|H]'


class FindingStatus(models.IntegerChoices):
    OPEN = 0, _("Open")
    FIXED = 1, _("Fixed")
    WONT_FIX = 2, _("Wont Fix")


class FindingQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(project=project)

    def for_report(self, project):
        return self.for_project(project).filter(exclude_from_report=False)

    def with_asset(self, asset):
        return self.filter(**{asset.asset_type: asset.pk})

    def with_severity(self, severity_name):
        severity = Severity[severity_name.upper()]
        return self.filter(severity=severity)

    def is_fixed(self):
        return self.filter(status=FindingStatus.FIXED)

    def exclude_fixed(self):
        return self.exclude(status=FindingStatus.FIXED)


class FindingManager(models.Manager):
    def create_from_template(self, **data):
        cwe_ids_default = []
        template = None

        if "vuln_key" in data:
            template = ProjectVulnerability.objects.get_or_create_from_key(
                *data["vuln_key"]
            )
        elif "vulnerability" in data:
            template = data["vulnerability"]

        if template is not None:
            cwe_ids_default = template.cwe_id
            defaults_from_template = ["severity"]
            for key in defaults_from_template:
                data.setdefault(key, getattr(template, key))
            # if template is global template use localization
            if not isinstance(template, ProjectVulnerability):
                localized = template.get_localized(data['project'].language)
                data.update({
                    "name": localized.name,
                    'recommendation': localized.recommendation,
                    'remediation': localized.remediation,
                    'description': localized.description
                })

        cwe_id = data.pop("cwe_ids", cwe_ids_default)
        finding = self.create(**data)
        finding.cwe_id = cwe_id
        return finding

    def copy_from_finding(self, finding):
        obj = self.model.objects.get(pk=finding.pk)
        obj.pk = None
        obj.unique_id = None
        obj.save()
        for proof in finding.findingimageattachment_set.all():
            image_file = ImageFile(proof.image)
            new_proof = copy.copy(proof)
            new_proof.pk = None
            new_proof.finding = obj
            new_proof.image = image_file
            new_proof.save()
            obj.proof_text = obj.proof_text.replace(proof.get_preview_url(), new_proof.get_preview_url())
            obj.save()
        return obj


class Finding(models.Model):
    component_choices = models.Q(app_label="backend", model="webapplication") | \
                        models.Q(app_label="backend", model="service") | \
                        models.Q(app_label="backend", model="host") | \
                        models.Q(app_label="backend", model="mobileapplication") | \
                        models.Q(app_label="backend", model="thickclient") | \
                        models.Q(app_label="backend", model="genericasset")

    objects = FindingManager.from_queryset(FindingQuerySet)()
    project = models.ForeignKey(
        "backend.Project", editable=False, on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    vulnerability = models.ForeignKey(
        "backend.ProjectVulnerability", on_delete=models.CASCADE
    )
    severity = models.PositiveSmallIntegerField(choices=Severity.choices)
    recommendation = models.TextField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        choices=FindingStatus.choices, default=FindingStatus.OPEN
    )
    imported = models.BooleanField(default=False)
    finding_date = models.DateField(null=True, blank=True, default=None)
    name = models.CharField(max_length=256)
    user_account = models.ForeignKey(
        "backend.Account", on_delete=models.SET_NULL, null=True, blank=True
    )
    needs_review = models.BooleanField(default=False)
    cwe_ids = models.ManyToManyField(CWE, blank=True)
    user = models.ForeignKey("backend.User", null=True, on_delete=models.SET_NULL)
    # retesting fields
    exclude_from_report = models.BooleanField(default=False)
    date_retest = models.DateField(null=True, blank=True)
    retest_results = models.TextField(null=True, blank=True)

    # affected components
    component_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                               limit_choices_to=component_choices)
    component_object_id = models.PositiveSmallIntegerField()
    component = GenericForeignKey('component_content_type', 'component_object_id')

    proof_text = models.TextField(default="", blank=True)
    cvss_score_40 = models.CharField(max_length=255, null=True, blank=True, validators=[validators.RegexValidator(
        regex=CVSS_40_REGEX
    )])
    cvss_score_31 = models.CharField(max_length=255, null=True, blank=True, validators=[validators.RegexValidator(
        regex=CVSS_31_REGEX
    )])
    unique_id = models.CharField(max_length=16, blank=True)

    class Meta:
        ordering = ["-severity"]
        indexes = [
            models.Index(fields=['component_content_type', 'component_object_id'])
        ]
        unique_together = [
            ('unique_id', 'project')
        ]

    def __str__(self):
        return f"{self.vulnerability.name} ({self.component})"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_status = self.status

    @property
    def retested(self):
        if self.date_retest:
            return True
        return False

    @property
    def cvss40_score(self):
        return cvss4.CVSS4Calculator().from_string(self.cvss_score_40)

    @property
    def cvss31_score(self):
        c = cvss.CVSS3(self.cvss_score_31)
        return c.scores()[0], c.severities()[0]

    @property
    def authentication_required(self):
        if self.user_account is None:
            return False
        return True

    def save(self, *args, **kwargs):
        if not self.finding_date:
            self.finding_date = timezone.now()
        if not self.pk or not self.project:
            self.project = self.vulnerability.project
        if self.unique_id is None or self.unique_id == '':
            self.unique_id = self.create_unique_id()
        self.full_clean()
        return super().save(*args, **kwargs)

    def create_unique_id(self):
        last_id = self.project.finding_set.order_by('-unique_id').values('unique_id').first()
        if not last_id:
            count = 1
        else:
            count = int(last_id['unique_id'].split('-')[-1]) + 1
        unique_id = f'F-{count:05d}'
        return unique_id

    def clean(self):
        if not self.component:
            raise ValidationError({'component': 'component is required'})
        if self.component.project != self.project:
            raise ValidationError({"component": "component does not belong to project"})
        return super().clean()

    @property
    def vuln_key(self):
        return self.vulnerability.natural_key

    @vuln_key.setter
    def vuln_key(self, value):
        self.vulnerability = ProjectVulnerability.objects.get_or_create_from_key(*value)

    @property
    def report_proof_text(self):
        """
        to allow captions in the reports, we will inject some HTML,
        also we replace image with their base64 representation.
        we inject all these stuff in the markdown - before being rendered.
        This allows our injected data to be bleached before further used
        :return:
        """
        image_re = r'(?P<alt>!\[(?P<caption>[^\]]*)\])\((?P<filename>.*/projects/\d+/findings/\d+/attachments/(?P<attachment>\d+)/preview/+)(?=\"|\))\)'

        def attachment_replace(match):
            attachment_pk = match.group("attachment")
            qs = self.findingimageattachment_set.filter(pk=attachment_pk)
            if not qs.exists():
                # not an attachment for our finding! nice try!
                return match.group()
            attachment = qs.get()
            caption = match.group('caption')
            template = f"<div class='image-proof'><div class='image-container'><img src='{attachment.image_base64}'></div><div class='caption'><span class='figure-prefix'>Figure</span><span>{caption}</span></div></div>"
            return template

        proof_text = re.sub(image_re, attachment_replace, self.proof_text)
        return proof_text


@receiver(signals.post_save, sender=Finding)
def finding_timeline_on_save(sender, instance, created, **kwargs):
    # log that new finding was created
    if created:
        title = "created the finding"
        text = ""
        FindingTimeline.objects.create(
            title=title, text=text, finding=instance, user=instance.user
        )
        return


@receiver(signals.post_save, sender=Finding)
def notify_project_users_critical_finding(sender, instance, created, **kwargs):
    """
    notify users - with corresponding setting - when new critical finding is created
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        context = {
            "findingId": instance.pk, "projectId": instance.project.pk,
            "project": instance.project
        }
        for membership in instance.project.membership_set.filter(user__usersettings__notify_critical_findings=True):
            # do not notify expired memberships
            if not membership.active:
                membership.delete()
                continue
            context["user"] = membership.user
            async_task(mail.send_new_critical_finding_mail, context, membership.user.email)
