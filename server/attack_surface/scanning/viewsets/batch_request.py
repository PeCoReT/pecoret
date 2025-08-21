from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from attack_surface.authentication import ScannerAuth
from attack_surface.mixins import ScanFeatureDispatchMixin, ScanningAuthMixin
from attack_surface.permissions import ScanningPermission
from attack_surface.scanning.filters.scan_batch import ScanBatchRequestFilter
from attack_surface.scanning.models import ScanBatchRequest
from attack_surface.scanning.models.scan_batch import StatusChoices
from attack_surface.scanning.scheduler.scan_event import scanner_event_parser_task
from attack_surface.scanning.serializers.batch_request import (
    ScanBatchFetchSerializer,
    ScanBatchRequestSerializer,
    ScanBatchRequestUpdateSerializer,
    ScanBatchRequestListSerializer,
)
from attack_surface.scanning.serializers.scanner_event import ScannerEventSerializer
from pecoret.core import permissions
from pecoret.core.utils.schema import extend_viewset_schema
from pecoret.core.viewsets import PeCoReTModelViewSet


@extend_viewset_schema(
    tags=["Attack Surface Scanning"], verbose_name="scan batch request"
)
class ScanBatchRequestViewSet(
    ScanFeatureDispatchMixin, ScanningAuthMixin, PeCoReTModelViewSet
):
    serializer_class = ScanBatchRequestSerializer
    queryset = ScanBatchRequest.objects.all()
    permission_classes = [
        ScanningPermission(
            read_only_groups=[permissions.Groups.GROUP_PENTESTER],
            scanner_write=True,
            scanner_read=True,
        ),
    ]
    api_scope = "scope_attack_surface"
    search_fields = ["scan_template__name"]
    ordering_fields = ["date_created", "date_updated"]
    filterset_class = ScanBatchRequestFilter

    def get_serializer_class(self):
        if self.action in ["partial_update", "update"]:
            return ScanBatchRequestUpdateSerializer
        elif self.action == "list":
            return ScanBatchRequestListSerializer
        elif self.action == "fetch_next_scan":
            return ScanBatchFetchSerializer
        return self.serializer_class

    @action(
        methods=["GET"],
        detail=False,
        permission_classes=[ScanningPermission(scanner_read=True, scanner_write=True)],
        authentication_classes=[ScannerAuth],
    )
    def fetch_next_scan(self, request, *args, **kwargs):
        scan_types = request.GET.getlist("type[]")

        with transaction.atomic():
            # Get all pending scan batches (based on your actual model, adjust the query)
            scan_batches = ScanBatchRequest.objects.select_for_update(
                skip_locked=True
            ).with_status_pending()
            # Apply scan type filter if provided
            if scan_types:
                scan_batches = scan_batches.filter(
                    scan_template__scan_type__in=scan_types
                )

            # Prioritize by the scan's priority and date created (oldest first if same priority)
            scan_batches = scan_batches.order_by(
                "-scan_template__priority", "date_created"
            )

            # Retrieve the highest priority scan batch available
            scan_batch = scan_batches.first()

            if scan_batch:
                # Mark the scan batch as in-progress
                scan_batch.status = StatusChoices.IN_PROGRESS
                scan_batch.save()

                # Return the scan batch data
                serializer = self.get_serializer(scan_batch)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # No available scan batches
        return Response({}, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[ScanningPermission(scanner_read=False, scanner_write=True)],
        authentication_classes=[ScannerAuth],
    )
    def result(self, request, *args, **kwargs):
        # this endpoint is handling scanner events
        serializer = ScannerEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event_type = serializer.validated_data["event_type"]
        scanner_event_parser_task(kwargs["pk"], event_type, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
