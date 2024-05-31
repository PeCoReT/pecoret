from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import viewsets


app_name = 'attack_surface'


router = DefaultRouter()
router.register('programs', viewsets.ProgramViewSet, 'program')
router.register('scan-findings', viewsets.ScanFindingViewSet, 'scan-finding')
router.register('urls', viewsets.URLViewSet, 'url')
router.register('targets', viewsets.TargetViewSet, 'target')
router.register('tags', viewsets.TagViewSet, 'tag')
router.register('ports', viewsets.PortViewSet, 'port')


urlpatterns = [
    path('attack-surface/', include(router.urls))
]
