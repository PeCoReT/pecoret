from django.apps import AppConfig


class AttackSurfaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attack_surface'

    def ready(self):
        from . import signals
