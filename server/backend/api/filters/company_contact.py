from django_filters import rest_framework as filters
from backend.models.company_contact import CompanyContact
from backend.models.company import Company


class CompanyContactFilter(filters.FilterSet):
    company = filters.ModelChoiceFilter(queryset=Company.objects.all())

    class Meta:
        model = CompanyContact
        fields = {
            "company": ["exact"]
        }
