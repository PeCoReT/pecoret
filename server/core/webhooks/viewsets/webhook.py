from rest_framework.permissions import IsAuthenticated

from core.webhooks.models import Webhook
from core.webhooks.serializers.webhook import WebhookSerializer
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet


@extend_viewset_schema(tags=['Webhooks'], verbose_name='webhook')
class WebhookViewSet(PeCoReTModelViewSet):
    queryset = Webhook.objects.none()
    serializer_class = WebhookSerializer
    permission_classes = (IsAuthenticated,)
    api_scope = None
    ordering_fields = ['date_created', 'date_updated']
    search_fields = ['url']

    def get_queryset(self):
        return Webhook.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
