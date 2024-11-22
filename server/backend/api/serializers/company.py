from rest_framework import serializers

from backend.models import Company


class CompanyMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['pk', 'date_created', 'date_updated', 'name']


class CompanySerializer(CompanyMinimalSerializer):
    class Meta:
        model = Company
        fields = CompanyMinimalSerializer.Meta.fields + ['street', 'zipcode', 'city', 'country', 'report_template',
                                                         'logo', 'has_logo']
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
    report_template = serializers.CharField(read_only=True)

    class Meta:
        fields = CompanySerializer.Meta.fields
        model = Company
