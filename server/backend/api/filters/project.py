from django_filters import rest_framework as filters
from pecoret.core.utils.filters import ChoiceFilter
from backend.models.project import Project, ProjectStatus
from backend.models.pinned_project import PinnedProject


class ProjectFilter(filters.FilterSet):
    status = ChoiceFilter(choices=ProjectStatus.choices)
    pinned = filters.BooleanFilter(method='filter_pinned')

    class Meta:
        model = Project
        fields = ["status", "pinned"]

    def filter_pinned(self, queryset, name, value):
        pinned_projects = PinnedProject.objects.for_user(self.request.user).values("project__pk")
        if value is True:
            return queryset.filter(pk__in=pinned_projects)
        return queryset.exclude(pk__in=pinned_projects)
