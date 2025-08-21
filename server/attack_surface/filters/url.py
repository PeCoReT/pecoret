from django_filters import rest_framework as filters
from django_filters import widgets
from attack_surface.models.url import URL
from attack_surface.models.service import Service
from attack_surface.models.program import Program
from .base import TagTechnologyFilter, ProgramFilterMixin


class URLFilter(ProgramFilterMixin, TagTechnologyFilter):
    service = filters.ModelChoiceFilter(field_name='service', queryset=Service.objects.all())
    program = filters.ModelMultipleChoiceFilter(widget=widgets.QueryArrayWidget, queryset=Program.objects.all(), method='filter_program')

    def filter_program(self, queryset, _name, value):
        if value:
            queryset = queryset.filter(service__target__program__in=value)
        return queryset

    class Meta:
        model = URL
        fields = [
            'is_base', 'tags', 'technologies', 'url', 'status_code', 'service', 'program'
        ]
