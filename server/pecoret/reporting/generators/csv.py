from .base import ReportGenerator


class CSVGenerator(ReportGenerator):
    content_type = 'text/plain'
    file_extension = 'csv'

    def generate(self, entry):
        self._preprocess()
        rendered = self.jinja_env.get_template(entry).render(self.context)
        rendered = self._postprocess(rendered)
        return rendered.encode(), self.content_type, self.file_extension
