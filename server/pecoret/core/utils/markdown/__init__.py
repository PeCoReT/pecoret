from django.utils.safestring import mark_safe

from . import constants
from .renderer import MarkdownHTMLRenderer


def markdown2html(markdown_content, limited=True):
    md_renderer = MarkdownHTMLRenderer(limited=limited)
    return mark_safe(md_renderer.render(markdown_content))
