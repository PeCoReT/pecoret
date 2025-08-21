from django.db import models
from pecoret.core.models import TimestampedModel, CASCADE_USER_TO_GHOST


class FindingCommentQuerySet(models.QuerySet):
    def for_finding(self, finding):
        return self.filter(finding=finding)

    def for_project(self, project):
        return self.filter(finding__project=project)


class FindingComment(TimestampedModel):
    objects = FindingCommentQuerySet.as_manager()
    user = models.ForeignKey('backend.User', on_delete=CASCADE_USER_TO_GHOST)
    comment = models.TextField()
    finding = models.ForeignKey('backend.Finding', on_delete=models.CASCADE)
    user_edit = models.ForeignKey('backend.User', null=True, blank=True, on_delete=CASCADE_USER_TO_GHOST,
                                  related_name='finding_comment_edited_set')

    class Meta:
        ordering = ["date_created"]
