from pecoret.core.serializers import ValuedChoiceField, VulnerabilityTemplateIdField
from advisories.serializers.advisory import BaseAdvisorySerializer
from advisories import fields
from backend.serializers.vulnerability import VulnerabilityTemplateSerializer
from backend.models.advisory import AdvisoryStatusChoices, VisibilityChoices, VulnerabilityStatusChoices
from .label import LabelSerializer


class AdvisoryAdvisoryManagementSerializer(BaseAdvisorySerializer):
    """
    an ``AdvisorySerializer`` which adds more fields used by the AdvisoryManagement
    """
    labels = LabelSerializer(many=True, read_only=True)
    vulnerability = VulnerabilityTemplateSerializer()
    status = ValuedChoiceField(choices=AdvisoryStatusChoices.choices)
    vulnerability_status = ValuedChoiceField(choices=VulnerabilityStatusChoices.choices)
    visibility = ValuedChoiceField(choices=VisibilityChoices.choices)

    class Meta(BaseAdvisorySerializer.Meta):
        fields = BaseAdvisorySerializer.Meta.fields + [
            "status", "vulnerability", "cve_id", "visibility", 'vulnerability_status',
            "date_disclosure", "date_planned_disclosure", "labels"
        ]


class AdvisoryManagementUpdateSerializer(BaseAdvisorySerializer):
    vulnerability = VulnerabilityTemplateSerializer(read_only=True)
    status = ValuedChoiceField(choices=AdvisoryStatusChoices.choices)
    vulnerability_status = ValuedChoiceField(choices=VulnerabilityStatusChoices.choices)
    visibility = ValuedChoiceField(choices=VisibilityChoices.choices)
    labels = fields.LabelField(serializer=LabelSerializer, many=True)
    vulnerability_id = VulnerabilityTemplateIdField(source="vulnerability_key")

    class Meta(BaseAdvisorySerializer.Meta):
        fields = BaseAdvisorySerializer.Meta.fields + [
            "status", "vulnerability", "cve_id", "visibility", 'vulnerability_status',
            "date_disclosure", "date_planned_disclosure", "labels",
            "vulnerability_id"
        ]
