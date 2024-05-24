from django_filters import widgets
from django_filters import rest_framework as filters
from asmonitor.models import URL, Tag
from backend.models.technology import Technology


class URLFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        widget=widgets.QueryArrayWidget, queryset=Tag.objects.all())
    technologies = filters.ModelMultipleChoiceFilter(
        widget=widgets.QueryArrayWidget, queryset=Technology.objects.all()
    )

    class Meta:
        model = URL
        fields = ['is_base', 'tags', 'technologies', ]
