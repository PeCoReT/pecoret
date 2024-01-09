from django.db import models
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.core.exceptions import PermissionDenied, ValidationError
from django.conf import settings


class ReportTemplateStatus(models.IntegerChoices):
    ACTIVE = 0, "Active"
    DRAFT = 1, "Draft"
    DEACTIVATED = 2, "Deactivated"


class ReportTemplateQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=ReportTemplateStatus.ACTIVE)


class ReportTemplate(models.Model):
    objects = ReportTemplateQuerySet.as_manager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(choices=ReportTemplateStatus.choices,
                                              default=ReportTemplateStatus.ACTIVE)
    name = models.CharField(max_length=64, unique=True, validators=[RegexValidator(r'^[\w\_]*$')])

    def __str__(self):
        return self.name

    def __init__(self, *args , **kwargs):
        super().__init__(*args, **kwargs)
        self.old_name = self.name

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        if self.old_name == "default_template" and self.old_name != self.name:
            raise ValidationError({"name": "cannot change name of default template"})
        return super().clean()

    @property
    def template_path(self):
        """the path of the ``templates`` subdirectory of the report template.

        Returns:
            str: path of the ``templates`` directory containing the jinja2 templates.
        """
        path = f'{self.name}/templates'
        return str(path)

    class Meta:
        ordering = ["-date_created", "name"]


@receiver(models.signals.pre_delete, sender=ReportTemplate)
def prevent_default_template_delete(sender, instance, **kwargs):
    if instance.name == "default_template":
        raise PermissionDenied("Default template cannot be removed")
