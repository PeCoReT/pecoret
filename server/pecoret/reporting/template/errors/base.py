from urllib.parse import urljoin
from django.conf import settings


class ReportError:
    """Define a report error.
    report errors can be created if a specific part is not completed but required in the report.
    """

    def __init__(self, message, url=None, edit_link=None):
        self.message = message
        self.url = url
        self.edit_link = edit_link


class BaseErrorCheck:
    def check(self, context, **kwargs):
        raise NotImplementedError

    @staticmethod
    def create_error(message, url, edit_link=None):
        return ReportError(message, url, edit_link=edit_link)

    @staticmethod
    def _build_url(path):
        url = settings.SITE_URL
        return urljoin(url, path)
