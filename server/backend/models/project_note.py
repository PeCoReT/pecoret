from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from pecoret.core.models import TimestampedModel
from pecoret.core.models.locked_model import LockedModel
from backend.models.object_lock import ObjectLock


class ProjectNoteQuerySet(models.QuerySet):
    def for_project(self, project):
        return self.filter(project=project)


class ProjectNote(TimestampedModel, LockedModel):
    objects = ProjectNoteQuerySet.as_manager()
    project = models.ForeignKey('backend.Project', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = models.TextField(default="", blank=True)
    object_lock = GenericRelation(ObjectLock, object_id_field='object_id', related_query_name='project_note',
                                  content_type_field='content_type')

    class Meta:
        ordering = ["title"]
        unique_together = [
            ('project', 'title')
        ]
