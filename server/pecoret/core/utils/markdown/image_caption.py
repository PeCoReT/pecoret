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
    allowed_dirs = [
        'uploads/attack_surface',
        'uploads/advisories'
    ]

    def _src_to_base64(self, src):
        """ map storage:/// urls to base64 rendered images """
        if not src.startswith('storage:///'):
            # not a storage url, do not process src
            return src
        src = src[len('storage:///'):]
        # check path traversal
        is_sub_dir = False
        for allowed_dir in self.allowed_dirs:
            allowed_dir = settings.BASE_DIR / allowed_dir
            try:
                r = Path(BASE_DIR / src).relative_to(allowed_dir)
                is_sub_dir = True
                break
            except ValueError:
                pass
        # possible path traversal attempt, return src instead of reading file
        if not is_sub_dir:
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
