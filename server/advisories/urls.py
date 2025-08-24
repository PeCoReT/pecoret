from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import viewsets

app_name = "advisories"

router = DefaultRouter()


# advisory core routes
router.register("advisories", viewsets.AdvisoryViewSet, "advisory")
router.register("advisory-labels", viewsets.LabelViewSet, "advisory-label")


# advisory routes
advisory_router = DefaultRouter()
advisory_router.register("timelines", viewsets.AdvisoryTimelineViewSet, "timeline")
advisory_router.register("attachments", viewsets.ImageAttachmentViewSet, "attachment")
advisory_router.register("share-tokens", viewsets.ShareTokenViewSet, "share-token")


urlpatterns = [
    path("", include(router.urls)),
    path("advisories/<int:advisory>/", include(advisory_router.urls)),
]
