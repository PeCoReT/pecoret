from .base import ReportGenerator


class ExcelGenerator(ReportGenerator):
    content_type = 'application/vnd.ms-excel'
    file_extension = 'xlsx'

    def generate(self, entry):
        raise NotImplementedError
