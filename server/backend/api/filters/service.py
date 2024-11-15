from django_filters import rest_framework as filters
from backend.models.assets.service import Service, Protocol, State
from backend.models.assets.host import Host
from pecoret.core.utils.filters import ChoiceFilter, filter_model_by_project


class ServiceFilter(filters.FilterSet):
    """filter for project asset ``service``

    Args:
        filters (_type_): _description_
    """
    state = ChoiceFilter(choices=State.choices)
    protocol = ChoiceFilter(choices=Protocol.choices)
    host = filters.ModelChoiceFilter(field_name="host", queryset=filter_model_by_project(Host))

    class Meta:
        model = Service
        fields = {
            "name": ["exact"],
            "host_id": ["exact"],
            "port": ["exact"],
            "protocol": ["exact"],
            "state": ["exact"]
        }
