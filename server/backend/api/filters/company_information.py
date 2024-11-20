from django_filters import rest_framework as filters
from backend.models.company_information import CompanyInformation
from backend.models.company import Company


class CompanyInformationFilter(filters.FilterSet):
    company = filters.ModelChoiceFilter(queryset=Company.objects.all())

    class Meta:
        model = CompanyInformation
        fields = {
            "company": ["exact"]
        }
