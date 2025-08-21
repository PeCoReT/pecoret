from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models


class UserQuerySet(models.QuerySet):
    pass


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    pass


class User(AbstractUser):
    """
    Custom user class with unique emails
    """
    objects = UserManager()
    email = models.EmailField(unique=True)
    new_email = models.EmailField(null=True, blank=True)
    nickname = models.CharField(max_length=64, null=True)
    company = models.ForeignKey('backend.Company', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ["username"]

    @property
    def report_display_name(self):
        if not self.nickname:
            return f'{self.first_name} {self.last_name}'
        return self.nickname

    @property
    def is_customer(self):
        return self.groups.filter(name="Customer").exists()

    @property
    def is_management_member(self):
        return self.groups.filter(name='Management').exists()

    @property
    def is_pentester_or_management(self):
        return self.groups.filter(models.Q(name='Management') | models.Q(name='Pentester')).exists()

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.username == 'Ghost':
            raise ValidationError({'username': 'Ghost user cannot be removed'})
        return super().delete(using=using, keep_parents=keep_parents)

    def clean(self):
        if self.username == 'Ghost':
            if self.is_active is True:
                raise ValidationError({'is_active': 'Ghost user cannot be activated'})
        if self.company and not self.is_customer:
            raise ValidationError({'company': 'Only customer group members can have a company set'})
        return super().clean()

    def is_markdown_limited(self):
        if self.groups.filter(name__in=['Management', 'Pentester']).exists():
            return False
        return True
