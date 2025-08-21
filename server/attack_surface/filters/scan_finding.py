from attack_surface.models.scan_finding import ScanFinding, Severity, ScanFindingStatus
from pecoret.core.utils.filters import ChoiceFilter
from .base import TagTechnologyFilter


class ScanFindingFilter(TagTechnologyFilter):
    severity = ChoiceFilter(choices=Severity.choices)
    status = ChoiceFilter(choices=ScanFindingStatus.choices)

    class Meta:
        model = ScanFinding
        fields = [
            'tags', 'technologies', 'tool', 'false_positive', 'severity', 'status'
        ]
