from django_filters import widgets
from django_filters import rest_framework as filters
from asmonitor.models import Host, Tag
from backend.models.technology import Technology


class HostFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        widget=widgets.QueryArrayWidget, queryset=Tag.objects.all())
    technologies = filters.ModelMultipleChoiceFilter(
        widget=widgets.QueryArrayWidget, queryset=Technology.objects.all()
    )

    class Meta:
        model = Host
        fields = ['tags', 'technologies']
