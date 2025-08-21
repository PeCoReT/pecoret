from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


class AccessChoices(models.IntegerChoices):
    NO_ACCESS = 0, "No Access"
    READ = 1, "Read"
    READ_WRITE = 2, "Read Write"


class APITokenQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)


class APITokenManager(models.Manager):

    def create_token(self, **data):
        data.pop('pk', None)
        data.pop('prefix', None)
        obj = self.model(**data)
        prefix = get_random_string(self.model.PREFIX_LENGTH)
        key = get_random_string(self.model.TOKEN_LENGTH)
        hashed_key = make_password(key)
        obj.pk = prefix
        obj.key = hashed_key
        obj.save()
        token = f"{prefix}.{key}"
        return obj, token

    def get_from_key(self, key: str):
        prefix, _, key_part = key.partition(".")
        queryset = self.all()

        try:
            api_key = queryset.get(prefix=prefix)
        except self.model.DoesNotExist:
            raise
        if not api_key.is_valid(key_part):
            raise self.model.DoesNotExist("Key is not valid.")
        else:
            return api_key


class APIToken(models.Model):
    TOKEN_LENGTH = 72
    PREFIX_LENGTH = 32

    objects = APITokenManager.from_queryset(APITokenQuerySet)()

    date_created = models.DateTimeField(auto_now_add=True)
    date_last_used = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('backend.User', on_delete=models.CASCADE)
    date_expire = models.DateTimeField(blank=True, null=True)

    prefix = models.CharField(max_length=64, primary_key=True, editable=False)
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=255, editable=False)

    # not yet in use
    project = models.ForeignKey('backend.Project', on_delete=models.CASCADE, null=True)
    # scope
    scope_advisories = models.PositiveSmallIntegerField(choices=AccessChoices.choices, default=AccessChoices.NO_ACCESS)
    scope_companies = models.PositiveSmallIntegerField(choices=AccessChoices.choices, default=AccessChoices.NO_ACCESS)
    scope_all_projects = models.PositiveSmallIntegerField(choices=AccessChoices.choices,
                                                          default=AccessChoices.NO_ACCESS)
    scope_user = models.PositiveSmallIntegerField(choices=AccessChoices.choices, default=AccessChoices.NO_ACCESS)
    scope_attack_surface = models.PositiveSmallIntegerField(choices=AccessChoices.choices, default=AccessChoices.NO_ACCESS)
    scope_knowledgebase = models.PositiveSmallIntegerField(choices=AccessChoices.choices,
                                                           default=AccessChoices.NO_ACCESS)

    def is_expired(self):
        if not self.date_expire:
            return False
        return timezone.now() >= self.date_expire

    def is_valid(self, key: str) -> bool:
        return check_password(key, self.key)

    class Meta:
        ordering = ["name"]
