from django_filters import widgets
from django_filters import rest_framework as filters
from asmonitor.models import Target, Tag
from backend.models.technology import Technology


class TargetFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        widget=widgets.QueryArrayWidget, queryset=Tag.objects.all())
    technologies = filters.ModelMultipleChoiceFilter(
        widget=widgets.QueryArrayWidget, queryset=Technology.objects.all()
    )

    class Meta:
        model = Target
        fields = ['tags', 'technologies']
