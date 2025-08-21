from django.utils.safestring import mark_safe

from . import constants
from .renderer import MarkdownHTMLRenderer


def markdown2html(markdown_content, limited=True, safe=True):
    md_renderer = MarkdownHTMLRenderer(limited=limited)
    if safe:
        # mostly required for PDF gen
        return mark_safe(md_renderer.render(markdown_content))
    return md_renderer.render(markdown_content)
