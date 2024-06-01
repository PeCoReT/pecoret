from pecoret.core.utils.filters import ChoiceFilter
from attack_surface.models.target import Target, ScopeChoices, DataTypes
from .base import TagTechnologyFilter, ProgramFilterMixin


class TargetFilter(ProgramFilterMixin, TagTechnologyFilter):
    scope = ChoiceFilter(choices=ScopeChoices.choices)
    data_type = ChoiceFilter(choices=DataTypes.choices)

    class Meta:
        model = Target
        fields = [
            'tags', 'technologies', 'data', 'data_type', 'scope', 'program'
        ]
