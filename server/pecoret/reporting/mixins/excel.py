from openpyxl import Workbook


class ExcelMixin:

    def __init__(self, *args, **kwargs):
        self.workbook = Workbook()

    def render_excel(self, context):
        raise NotImplementedError()
