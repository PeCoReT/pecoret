from .base import ReportGenerator


class MarkdownGenerator(ReportGenerator):
    content_type = 'text/plain'
    file_extension = 'md'

    def generate(self, entry):
        self._preprocess()
        rendered = self.jinja_env.get_template(entry).render(self.context)
        self._postprocess(rendered)
        return rendered, self.content_type, self.file_extension
