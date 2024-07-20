import os

import sass
import weasyprint
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from .base import ReportGenerator


class PDFReportGenerator(ReportGenerator):
    content_type = 'application/pdf'
    file_extension = 'pdf'

    def __init__(self, report_plugin, context, language=None, **kwargs):
        super().__init__(report_plugin, context, language=language, **kwargs)
        self.font_config = FontConfiguration()
        self.css_files = []

    def url_fetcher(self, url, *args, **kwargs):
        if url.startswith("file://"):
            media_name = url.replace("file://", "")
            media_path = self.get_filepath(media_name)
            return {"file_obj": open(media_path, "rb")}
        return weasyprint.default_url_fetcher(url, *args, **kwargs)

    def get_stylesheets(self):
        css_paths = []
        for css in self.css_files:
            if not str(css).startswith('/'):
                new_css_path = os.path.join(self.report_plugin.templates_directory, css)
            else:
                new_css_path = css
            css_paths.append(new_css_path)
        # append sass files
        sass_path = os.path.join(self.report_plugin.templates_directory, "scss/main.scss")
        if os.path.exists(sass_path):
            compiled_scss = sass.compile(filename=sass_path, output_style="compressed")
            css_paths.append(
                CSS(
                    string=compiled_scss,
                    font_config=self.font_config,
                    url_fetcher=self.url_fetcher,
                )
            )
        return css_paths

    def generate(self, entry):
        self._preprocess()
        rendered_template = self.jinja_env.get_template(entry).render(self.context)
        weasy_html = HTML(string=rendered_template, url_fetcher=self.url_fetcher)
        weasy_pdf = weasy_html.write_pdf(
            stylesheets=self.get_stylesheets(), font_config=self.font_config,
            optimize_images=True  # required to prevent weasyprint crashes in >=v59
        )
        self._postprocess(weasy_pdf)
        return weasy_pdf, self.content_type, self.file_extension

    def get_filepath(self, filename):
        return self.report_plugin.get_filepath(filename)

