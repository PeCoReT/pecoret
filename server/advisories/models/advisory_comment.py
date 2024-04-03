from django.db import models

from pecoret.core.models import TimestampedModel, CASCADE_USER_TO_GHOST


class AdvisoryCommentQuerySet(models.QuerySet):
    def for_advisory(self, advisory):
        return self.filter(advisory=advisory)


class AdvisoryComment(TimestampedModel):
    objects = AdvisoryCommentQuerySet.as_manager()
    advisory = models.ForeignKey('advisories.Advisory', on_delete=models.CASCADE)
    comment = models.TextField()
    user = models.ForeignKey('backend.User', on_delete=models.SET_NULL, null=True)
    user_edit = models.ForeignKey('backend.User', null=True, blank=True, on_delete=CASCADE_USER_TO_GHOST,
                                  related_name='advisory_comment_edited_set')

    def __str__(self):
        return str(self.advisory)

    class Meta:
        ordering = ["date_created"]
        db_table = 'backend_advisorycomment'
