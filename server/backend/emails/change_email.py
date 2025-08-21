from django.conf import settings
from pecoret.core import utils
from backend.utils.change_email_token_generator import change_email_token_generator
from .base import TemplatedBaseMail


class ChangeEmail(TemplatedBaseMail):
    """this template is used for the password reset mail
    """
    template_name = "emails/change_email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = change_email_token_generator.make_token(user)
        context["url"] = settings.SITE_URLS.get("CHANGE_EMAIL").format(**context)
        return context
