from django.db.models import signals, Count
from django.dispatch import receiver

from attack_surface import models
from attack_surface.utils.scoping import check_target_scope, check_scope_for_program


@receiver(signals.post_save, sender=models.Target)
def target_scope_validation(sender, instance, created, **kwargs):
    # if a new target is created, check its scope status based on `ScopeItem`s
    if created:
        check_target_scope(instance)


@receiver(signals.m2m_changed, sender=models.URL.technologies.through)
def sync_url_technologies(sender, instance, action, reverse, model, pk_set, **kwargs):
    """
    sync url technologies to parent service
    # TODO: how to trigger this also when service changes without getting recursion errors
    """
    service = instance.service
    for technology in instance.technologies.all():
        service.technologies.add(technology)
    service.save()


@receiver(signals.post_save, sender=models.ScopeItem)
def revalidate_scope(sender, instance, created, **kwargs):
    # revalidate scope if a `ScopeItem` is saved
    check_scope_for_program(instance.scope.program)

@receiver(signals.post_delete, sender=models.ScopeItem)
def revalidate_scope_on_delete(sender, instance, **kwargs):
    # Revalidate scope if a ScopeItem is deleted
    check_scope_for_program(instance.scope.program)