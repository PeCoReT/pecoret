from django.dispatch import receiver
from django.db.models import signals
from django.conf import settings
from django_q.tasks import async_task

from attack_surface import models
from attack_surface.tasks import enqueue_for_scan_seed


@receiver(signals.post_save, sender=models.Host)
@receiver(signals.post_save, sender=models.Service)
@receiver(signals.post_save, sender=models.Target)
@receiver(signals.post_save, sender=models.URL)
@receiver(signals.post_save, sender=models.Port)
def queue_initial_scan(sender, instance, created, **kwargs):
    if not settings.AS_ENABLE_SCAN_ON_CREATION or not settings.AS_ENABLE_SCANNING:
        # feature disabled
        return
    if not created:
        return
    # TODO: only scan in-scope items
    async_task(enqueue_for_scan_seed, instance._meta.label, instance.pk)
