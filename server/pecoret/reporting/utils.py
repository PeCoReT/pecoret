from django.utils.translation import gettext as _


def dynamic_trans(data):
    """jinja does not properly support dynamic translation of variables.
    This is a workaround using a jinja filter
    """
    return _(data)
