import nh3
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from . import constants

from pecoret.core.utils.markdown.image_caption import ImageCaptionsExtension


class MarkdownHTMLRenderer:
    """
    this class renders markdown2html.
    we render custom storage:// protocol for "privileged" users.
    this means all external users like customers should be limited in features, to prevent abuse.
    """
    extensions = ['fenced_code', 'footnotes']

    def __init__(self, limited=True):
        self.limited = limited
        self.extensions = [
            'fenced_code', 'footnotes', 'tables',
            CodeHiliteExtension(
                guess_lang=False,
                linenums=False,
                lineos='inline',
                linespans='line',
                startinline=True
            )
        ]
        self.allowed_tags = constants.BASE_ALLOWED_TAGS
        self.allowed_attributes = constants.BASE_ALLOWED_ATTRIBUTES
        self.protocols = set()
        if not self.limited:
            self.allowed_attributes['img'] = {'src', 'alt'}
            self.protocols.add('storage')
            self.protocols.add('data')
            # allow not limited users to access storage://
            self.extensions.append(ImageCaptionsExtension())

    def render(self, text):
        """ render markdown2html """
        if not text:
            return ''
        md = markdown(text, extensions=self.extensions)
        return nh3.clean(md,
                         tags=set(self.allowed_tags),
                         attributes=self.allowed_attributes,
                         url_schemes=self.protocols)
