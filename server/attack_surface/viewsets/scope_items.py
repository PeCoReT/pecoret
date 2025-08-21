from rest_framework.decorators import action
from rest_framework.response import Response

from attack_surface.filters.scope import ScopeItemFilter
from attack_surface.models import ScopeItem
from attack_surface.permissions import ScanningPermission
from attack_surface.serializers.scope import ScopeSerializer
from attack_surface.serializers.scope_item import ScopeItemSerializer
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet


class ScopeItemsViewSet(PeCoReTModelViewSet):
    queryset = ScopeItem.objects.all()
    serializer_class = ScopeItemSerializer
    permission_classes = [
        ScanningPermission(
            read_write_groups=[permissions.Groups.GROUP_PENTESTER],
            read_only_groups=[],
            scanner_read=True,
            scanner_write=False,
        )
    ]
    api_scope = 'scope_attack_surface'
    search_fields = ['value', 'annotation']
    ordering_fields = ['date_created', 'date_updated']
    filterset_class = ScopeItemFilter

    @action(detail=False, methods=['get'])
    def group_items_by_scope(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Grouping items by scope
        grouped_items = {}
        for item in queryset:
            if item.scope not in grouped_items:
                grouped_items[item.scope] = []
            grouped_items[item.scope].append(ScopeItemSerializer(item).data)

        # Preparing the response data
        response_data = []
        for scope, items in grouped_items.items():
            scope_data = ScopeSerializer(scope).data
            response_data.append({'scope': scope_data, 'items': items})

        return Response(response_data)
