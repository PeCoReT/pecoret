import markdown
import nh3
from django.utils.safestring import mark_safe
from markdown.extensions.codehilite import CodeHiliteExtension


def bleach_md(markdown_content, allow_images=False):
    allowed_tags = [
        "p",
        "a",
        "code",
        "pre",
        "blockquote",
        "strong",
        "em",
        "br",
        "b",
        "i",
        "ul",
        "li",
        "div",
        "span",
        "h1", "h2", "h3", "h4", "h5", "h6"
                                      "sup",
        "ol",
        "hr",
        "table", "tr", "th", "thead", "tbody", "td"
    ]
    allowed_attributes = {
        "code": {"class"},
        "a": {"href"},
        "div": {"class"},
        "span": {"class"},
        "sup": {"id"},
        "table": {"class"}, "tr": {"class"}, "th": {"class"}, "td": {"class"}
    }
    protocols = set()
    if not markdown_content:
        return ""
    if allow_images:
        allowed_tags.append("img")
        allowed_attributes["img"] = {"alt", "src"}
        protocols.add("data")
    cleaned = nh3.clean(
        markdown.markdown(
            markdown_content,
            extensions=[
                "fenced_code",
                "footnotes",
                CodeHiliteExtension(
                    guess_lang=False,
                    linenums=True,
                    linenos="inline",
                    linespans="line",
                    startinline=True,
                )
            ],
        ),
        tags=set(allowed_tags),
        attributes=allowed_attributes,
        url_schemes=protocols,
    )
    return cleaned


def md_to_clean_html(content, allow_images=False):
    return mark_safe(bleach_md(content, allow_images=allow_images))
