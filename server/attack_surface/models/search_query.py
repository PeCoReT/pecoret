from django.db import models
from pecoret.core.models import TimestampedModel


class UserSearchQueryQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)


class UserSearchQuery(TimestampedModel):
    objects = UserSearchQueryQuerySet.as_manager()
    user = models.ForeignKey('backend.User', on_delete=models.CASCADE)
    query = models.CharField(max_length=1024)
    name = models.CharField(max_length=28)

    class Meta:
        unique_together = (('user', 'name'),)
        ordering = ['name']
