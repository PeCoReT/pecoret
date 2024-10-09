import base64
from pathlib import Path
from xml.etree import ElementTree
from django.conf import settings
from markdown.extensions import Extension
from markdown.inlinepatterns import LinkInlineProcessor

from pecoret.settings import BASE_DIR

CAPTION_RE = r'\!\[(?=[^\]]*\])'

# original source: https://github.com/Evidlo/markdown_captions
# simplified to match our needs more
# handle regular inline image: ![caption](storage:///uploads/img.jpg)
class ImageInlineProcessor(LinkInlineProcessor):

    def _src_to_base64(self, src):
        """ map storage:/// urls to base64 rendered images """
        allowed_dir = settings.BASE_DIR / 'uploads'
        if not src.startswith('storage:///'):
            # not a storage url, do not process src
            return src
        src = src[len('storage:///'):]
        # check path traversal
        try:
            Path(allowed_dir).joinpath(src).resolve().relative_to(allowed_dir.resolve())
        except ValueError:
            # possible path traversal attempt, return src instead of reading file
            return src
        path = Path(BASE_DIR / src)
        # file does not exist
        if not path.exists():
            return src
        with open(path, 'rb') as f:
            data = f.read()
            img = base64.b64encode(data).decode()
        return f'data:image/png;base64,{img}'

    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        src, title, index, handled = self.getLink(data, index)
        src = self._src_to_base64(src)

        if not handled:
            return None, None, None

        fig = ElementTree.Element('figure')
        img = ElementTree.SubElement(fig, 'img')
        cap = ElementTree.SubElement(fig, 'figcaption')

        img.set('src', src)

        if title is not None:
            img.set("title", title)

        cap.text = text
        return fig, m.start(0), index


class ImageCaptionsExtension(Extension):
    def extendMarkdown(self, content):
        content.inlinePatterns.register(
            ImageInlineProcessor(CAPTION_RE, content), 'caption', 151)
