from django_filters import widgets
from django_filters import rest_framework as filters
from asmonitor.models import Target, Tag


class TargetFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        widget=widgets.QueryArrayWidget, queryset=Tag.objects.all())

    class Meta:
        model = Target
        fields = ['tags']
