from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from advisories.filters import InboxFilter
from advisories.serializers.advisory_management import AdvisoryAdvisoryManagementSerializer
from backend.models import Advisory
from pecoret.core import mixins
from pecoret.core import permissions
from pecoret.core.viewsets import GenericViewSet


class AdvisoryManagementInboxViewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [permissions.PRESET_GROUP_ADVISORY_MANAGEMENT]
    filterset_class = InboxFilter
    search_fields = ["product", "vendor_name", "internal_name", "vulnerability__vulnerability_id"]
    ordering_fields = ["advisory_id", "date_planned_disclosure", "date_created", "date_updated"]
    serializer_class = AdvisoryAdvisoryManagementSerializer

    def get_queryset(self):
        return Advisory.objects.for_advisory_management()

    @action(detail=False, methods=["get"])
    def inbox_statistics(self, request, *args, **kwargs):
        qs = self.get_queryset()
        data = {
            "inbox_count": qs.count(),
            "inbox_unfixed_count": qs.unfixed().count(),
            "inbox_fixed_count": qs.fixed().count(),
            "inbox_wontfix_count": qs.wont_fix().count(),
            "inbox_next_disclosure_date": None
        }
        if qs.count() > 0:
            data["inbox_next_disclosure_date"] = qs.order_by("-date_planned_disclosure").first().date_planned_disclosure
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def top_submitters(self, request, *args, **kwargs):
        qs = self.get_queryset().count_by_user()
        return Response(list(qs)[:10])

    @action(detail=False, methods=["get"])
    def top_vulnerabilities(self, request, *args, **kwargs):
        qs = self.get_queryset().values("vulnerability__name").annotate(count=Count('pk')).order_by("-count")
        return Response(list(qs)[:10])

    @action(detail=False, methods=["get"])
    def top_products(self, request, *args, **kwargs):
        qs = self.get_queryset().values("technology__name", "technology__vendor").annotate(count=Count('pk')).order_by(
            "-count")
        return Response(list(qs)[:10])

    @action(detail=False, methods=["get"])
    def top_vendors(self, request, *args, **kwargs):
        qs = self.get_queryset().filter(technology__vendor__isnull=False).values("technology__vendor").annotate(
            count=Count('pk')).order_by("-count")
        return Response(list(qs)[:10])
