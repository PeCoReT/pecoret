from rest_framework import serializers
from pecoret.core.serializers import ActiveReportTemplateSerializerField
from backend.models import Company
from .report_templates import ReportTemplateMinimalSerializer


class CompanySerializer(serializers.ModelSerializer):
    report_template = ActiveReportTemplateSerializerField(serializer=ReportTemplateMinimalSerializer)

    class Meta:
        model = Company
        fields = [
            "pk",
            "date_created",
            "date_updated",
            "name",
            "street",
            "zipcode",
            "city",
            "country",
            "report_template",
            "logo"
        ]
        extra_kwargs = {
            "logo": {
                "write_only": True
            }
        }


class CustomerCompanySerializer(CompanySerializer):
    """
    customers should not be able to access/change some fields
    (e.g. report templates, which may reveal other customer names)
    """
    report_template = ActiveReportTemplateSerializerField(read_only=True, serializer=ReportTemplateMinimalSerializer)

    class Meta:
        fields = CompanySerializer.Meta.fields
        model = Company
