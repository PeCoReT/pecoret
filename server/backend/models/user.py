from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager


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
    company = models.ForeignKey('backend.Company', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ["username"]

    @property
    def report_display_name(self):
        if self.usersettings.show_real_name_in_report:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @property
    def is_customer(self):
        return self.groups.filter(name="Customer").exists()
