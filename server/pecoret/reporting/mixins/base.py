

class ContextMixin:
    def get_context(self):
        return {}


class FileDownloadMixin:
    file_extension = None
    content_type = None
