from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets

app_name = "webhooks"

router = DefaultRouter()
router.register('webhooks', viewsets.WebhookViewSet, 'webhook')

urlpatterns = [
    path('', include(router.urls))
]