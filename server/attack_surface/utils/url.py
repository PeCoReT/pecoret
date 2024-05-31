from urllib.parse import urlparse


def hostname_from_url(url: str) -> str:
    """
    extract hostname from url
    """
    return urlparse(url).hostname


def port_and_scheme_from_url(url: str) -> tuple:
    """
    get port from url
    """
    parsed = urlparse(url)
    if parsed.port:
        return parsed.scheme, parsed.port
    if parsed.scheme == 'https':
        port = 443
    else:
        port = 80
    return parsed.scheme, port
