from django_filters import widgets
from django_filters import rest_framework as filters

from attack_surface.models import Program
from attack_surface.models.tag import Tag
from backend.models.technology import Technology


class TagTechnologyFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        widget=widgets.QueryArrayWidget, queryset=Tag.objects.all())
    technologies = filters.ModelMultipleChoiceFilter(
        widget=widgets.QueryArrayWidget, queryset=Technology.objects.all()
    )


class ProgramFilterMixin:
    program = filters.ModelMultipleChoiceFilter(field_name='program', queryset=Program.objects.all(), widget=widgets.QueryArrayWidget)
