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
router.register('services', viewsets.ServiceViewSet, 'service')
router.register('asns', viewsets.ASNViewSet, 'asn')
router.register('search-queries', viewsets.UserSearchQueryViewSet, 'search-query')
router.register('findings', viewsets.FindingViewSet, 'finding')
router.register('finding-components', viewsets.FindingComponentViewSet, 'finding-component')

scan_router = DefaultRouter()
scan_router.register('scan-types', viewsets.ScanTypeViewSet, 'scan-type')
scan_router.register('scanners', viewsets.ScannerViewSet, 'scanner')
scan_router.register('scans', viewsets.ScanViewSet, 'scan')

urlpatterns = [
    path('attack-surface/', include(router.urls)),
    path('attack-surface/scanning/', include(scan_router.urls)),
]
