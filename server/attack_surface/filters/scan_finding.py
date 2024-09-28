from pecoret.core.utils.filters import ChoiceFilter
from attack_surface.models.scan_finding import ScanFinding, Severity, ScanFindingStatus
from .base import TagTechnologyFilter, ProgramFilterMixin


class ScanFindingFilter(ProgramFilterMixin, TagTechnologyFilter):
    severity = ChoiceFilter(choices=Severity.choices)
    status = ChoiceFilter(choices=ScanFindingStatus.choices)

    class Meta:
        model = ScanFinding
        fields = [
            'tags', 'technologies', 'program', 'tool', 'false_positive', 'severity', 'status'
        ]
