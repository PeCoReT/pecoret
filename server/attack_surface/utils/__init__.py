import tldextract
from . import url


def is_subdomain(domain):
    ext = tldextract.extract(domain)
    return bool(ext.subdomain)
