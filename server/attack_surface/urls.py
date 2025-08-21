from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import viewsets
from .scanning import viewsets as scanning_views

app_name = "attack_surface"

router = DefaultRouter()
router.register("programs", viewsets.ProgramViewSet, "program")
router.register("scan-findings", viewsets.ScanFindingViewSet, "scan-finding")
router.register("urls", viewsets.URLViewSet, "url")
router.register("targets", viewsets.TargetViewSet, "target")
router.register("tags", viewsets.TagViewSet, "tag")
router.register("services", viewsets.ServiceViewSet, "service")
router.register("asns", viewsets.ASNViewSet, "asn")
router.register("search-queries", viewsets.UserSearchQueryViewSet, "search-query")
router.register("findings", viewsets.FindingViewSet, "finding")
router.register(
    "finding-components", viewsets.FindingComponentViewSet, "finding-component"
)
router.register("finding-images", viewsets.FindingImageViewSet, "finding-image")

scan_router = DefaultRouter()
scan_router.register("scanners", scanning_views.ScannerViewSet, "scanner")

# scanning v2
scan_router.register("requests", scanning_views.ScanBatchRequestViewSet, "scan-request")
scan_router.register(
    "scan-templates", scanning_views.ScanTemplateViewSet, "scan-template"
)

# scoping
scoping_router = DefaultRouter()
scoping_router.register("scopes", viewsets.ScopeViewSet, "scope")
scoping_router.register("items", viewsets.ScopeItemsViewSet, "scope-item")


urlpatterns = [
    path("attack-surface/", include(router.urls)),
    path("attack-surface/scanning/", include(scan_router.urls)),
    path("attack-surface/scoping/", include(scoping_router.urls)),
]
