from django_filters import widgets
from django_filters import rest_framework as filters
from pecoret.core.utils.filters import ChoiceFilter
from advisories.models.label import Label
from backend.models.advisory import Advisory, AdvisoryStatusChoices


class InboxFilter(filters.FilterSet):
    status = ChoiceFilter(choices=AdvisoryStatusChoices.choices)
    # seems like `widgets.QueryArrayWidget` is required to have `labels[]=1` query syntax support
    labels = filters.ModelMultipleChoiceFilter(
        widget=widgets.QueryArrayWidget,
        queryset=Label.objects.all())

    class Meta:
        model = Advisory
        fields = ["status", "labels"]

    @property
    def qs(self):
        parent = super().qs
        return parent.for_advisory_management()
