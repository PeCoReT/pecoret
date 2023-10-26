from django.core.exceptions import ImproperlyConfigured
from .base import FileDownloadMixin


class ProjectRelatedMixin(FileDownloadMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report_document = kwargs.get('report_document')
        if not self.report_document:
            raise ImproperlyConfigured("report_document must be set")

    def get_project(self):
        return self.report_document.report.project

    def post_processing(self, rendered_report, *args, **kwargs):
        self.report_document.compiled_source = rendered_report
        self.report_document.content_type = self.content_type
        self.report_document.file_extension = self.file_extension
        self.report_document.save()
