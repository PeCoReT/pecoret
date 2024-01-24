from django.db.models import Count
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from backend.models import Project, Membership, PinnedProject
from backend.models.finding import Finding, Severity
from backend.models.membership import Roles
from backend.filters.project import ProjectFilter
from backend.serializers.project import ProjectSerializer
from backend.serializers.pinned_project import PinnedProjectSerializer
from pecoret.core import permissions
from pecoret.core.viewsets import PeCoReTModelViewSet


class ProjectViewSet(PeCoReTModelViewSet):
    queryset = Project.objects.none()
    filterset_class = ProjectFilter
    search_fields = ["name"]
    ordering_fields = ["name", "date_updated", "date_created"]
    api_scope = "scope_all_projects"
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        obj = serializer.save()
        Membership.objects.create(user=self.request.user, project=obj, role=Roles.OWNER)

    def get_permissions(self):
        if self.action == "create":
            return [permissions.PRESET_GROUP_MANAGEMENT()]
        elif self.action == "list":
            return [
                permissions.GroupPermission(
                    read_write_groups=[
                        permissions.Groups.GROUP_MANAGEMENT,
                        permissions.Groups.GROUP_PENTESTER
                    ],
                    read_only_groups=[permissions.Groups.CUSTOMER]
                )
            ]
        elif self.action == "destroy":
            return [permissions.PRESET_GROUP_MANAGEMENT()]
        elif self.action == "retrieve":
            return [permissions.PRESET_PENTESTER_OR_READONLY()]
        elif self.action == "token_check":
            return [
                permissions.GroupPermission(
                    read_only_groups=[
                        permissions.Groups.GROUP_MANAGEMENT,
                        permissions.Groups.GROUP_PENTESTER,
                    ],
                )()
            ]
        elif self.action == "available_languages":
            return [
                permissions.GroupPermission(
                    read_only_groups=[
                        permissions.Groups.GROUP_MANAGEMENT,
                        permissions.Groups.GROUP_PENTESTER,
                    ]
                )
            ]
        elif self.action == "pin_project":
            return [permissions.PRESET_PENTESTER_OR_READONLY]
        return [permissions.PRESET_OWNER_OR_READ_ONLY()]

    @action(methods=["get"], detail=True)
    def stats_finding_dashboard(self, request, *args, **kwargs):
        project = self.get_object()
        findings = (
            Finding.objects.for_project(project)
            .values("severity")
            .annotate(count=Count("pk"))
            .order_by("-severity")
        )
        data = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Informational": 0}
        for finding in findings:
            data[Severity(finding["severity"]).label] = finding["count"]
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="available-languages")
    def available_languages(self, request, *args, **kwargs):
        data = []
        for lang in settings.LANGUAGES:
            data.append({"language": lang[1], "code": lang[0]})
        return Response(data)

    @action(detail=True, methods=["post", "delete"], serializer_class=PinnedProjectSerializer)
    def pin_project(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = PinnedProjectSerializer(data=request.data)
        if serializer.is_valid():
            if request.method.lower() == "post":
                PinnedProject.objects.create(user=request.user, project=obj)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method.lower() == "delete":
            PinnedProject.objects.for_user(request.user).for_project(obj).delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
