import os

import sass
import weasyprint
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

from .jinja import JinjaMixin


class PDFMixin(JinjaMixin):
    _css_files = []
    _sass_files = []
    content_type = "application/pdf"
    file_extension = "pdf"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font_config = FontConfiguration()

    def get_css_files(self):
        return self._css_files.copy()

    def get_sass_files(self):
        return self._sass_files.copy()

    def get_sass_directory(self):
        """
        get the root path of the sass files
        :return:
        """
        return self.template_path

    def get_css_directory(self):
        return self.template_path

    def get_file_url_path(self):
        return self.template_path

    def get_stylesheets(self):
        css_paths = set()
        for css in self.get_css_files():
            new_css_path = os.path.join(self.get_css_directory(), css)
            css_paths.add(new_css_path)
        # append sass files
        sass_path = os.path.join(self.template_path, "scss/main.scss")
        if os.path.exists(sass_path):
            compiled_sass = sass.compile(filename=sass_path, output_style="compressed")
            css_paths.add(
                CSS(string=compiled_sass, font_config=self.font_config, url_fetcher=self.url_fetcher)
            )
        for sass_file in self.get_sass_files():
            full_path = os.path.join(self.get_sass_directory(), sass_file)
            compiled_sass = sass.compile(filename=full_path, output_style="compressed")
            css_paths.add(
                CSS(string=compiled_sass, font_config=self.font_config, url_fetcher=self.url_fetcher)
            )
        return list(css_paths)

    def url_fetcher(self, url, *args, **kwargs):
        if url.startswith("file://"):
            media_name = url.replace("file://", "")
            media_path = os.path.join(self.template_path, media_name)
            return {"file_obj": open(media_path, "rb")}
        return weasyprint.default_url_fetcher(url, *args, **kwargs)

    def render_pdf(self, context):
        rendered_string = self.render_to_string(context)
        html = HTML(string=rendered_string, url_fetcher=self.url_fetcher)
        pdf = html.write_pdf(
            stylesheets=self.get_stylesheets(), font_config=self.font_config,
            optimize_images=True  # required to prevent weasyprint crashes in >=59
        )
        return pdf
