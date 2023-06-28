from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets

app_name = "advisories"

router = DefaultRouter()

router.register("inbox", viewsets.AdvisoryManagementInboxViewSet, "inbox")

urlpatterns = [
    path('advisory-management/', include(router.urls))
]
