from django.conf import settings
from django.utils.translation import gettext as _


def dynamic_trans(data):
    """jinja does not properly support dynamic translation of variables.
    This is a workaround using a jinja filter
    """
    return _(data)


def get_report_template_choices():
    """
    return a tuple required for model choicefields for templates
    """
    return {i: i for i in settings.REPORT_TEMPLATES}
