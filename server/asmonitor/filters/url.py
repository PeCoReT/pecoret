from django_filters import rest_framework as filters
from asmonitor.models import URL


class URLFilter(filters.FilterSet):

    class Meta:
        model = URL
        fields = ['is_base']
