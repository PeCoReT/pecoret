from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import signals, Count
from django.dispatch import receiver
from django_q.tasks import async_task

from attack_surface import models
from attack_surface.models import Scan
from attack_surface.tasks import enqueue_for_scan_seed


@receiver(signals.post_save, sender=models.Service)
@receiver(signals.post_save, sender=models.Target)
@receiver(signals.post_save, sender=models.URL)
def queue_initial_scan(sender, instance, created, **kwargs):
    if not settings.AS_ENABLE_SCAN_ON_CREATION or not settings.AS_ENABLE_SCANNING:
        # feature disabled
        return
    if not created:
        return
    if not instance.is_in_scope:
        # only scan in-scope items on creation
        return
    async_task(enqueue_for_scan_seed, instance._meta.label, instance.pk)


@receiver(signals.pre_delete, sender=models.Service)
@receiver(signals.pre_delete, sender=models.Target)
@receiver(signals.pre_delete, sender=models.URL)
def delete_scan_when_empty(sender, instance, **kwargs):
    ct = ContentType.objects.get_for_model(instance)
    scans = Scan.objects.annotate(count=Count('scanobject__pk')).filter(count__lte=1, scanobject__object_id=instance.pk,
                                                                        scanobject__content_type=ct)
    scans.delete()
