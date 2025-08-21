from django_filters.filters import ChoiceFilter as BaseChoiceFilter
from django.forms.fields import ChoiceField as BaseChoiceField
from django.core.exceptions import ValidationError


def filter_model_by_project(model):
    """filter queryset by project when model has project field
    """
    def filtered(request):
        if hasattr(request, "project"):
            return model.objects.for_project(request.project)
        return model.objects.all()
    return filtered


class ChoiceField(BaseChoiceField):
    """override the to_python method to allow filtering on values instead of keys
    this makes it possible to have `status=Open`  instead of `status=1`
    """
    def to_python(self, value):
        if value in self.empty_values:
            return None
        for k, v in self.choices:
            if str(v) == str(value):
                return k
        raise ValidationError("Invalid value!")


class ChoiceFilter(BaseChoiceFilter):
    """filter that utilizes custom ChoiceField.
    this makes it possible to have `status=Open`  instead of `status=1`
    """
    field_class = ChoiceField
