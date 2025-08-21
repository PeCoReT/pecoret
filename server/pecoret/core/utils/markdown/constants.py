BASE_ALLOWED_TAGS = [
    'p', 'a', 'code', 'pre', 'blockquote', 'strong', 'em', 'br', 'b', 'i',
    # lists
    'ul', 'li', 'ol',
    'div', 'span', 'sub',
    # headings
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'hr',
    # tables
    'table', 'tr', 'th', 'td', 'thead', 'tbody',
    # figures
    'figcaption', 'figure',
    # images
    'img'
]

BASE_ALLOWED_ATTRIBUTES = {
    "code": {"class"},
    "a": {"href"},
    "div": {"class"},
    "span": {"class"},
    "sup": {"id"},
    "table": {"class"}, "tr": {"class"}, "th": {"class"}, "td": {"class"},
    'img': {'alt'},
    'pre': {'class'},
}
