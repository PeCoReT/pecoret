import tldextract
from . import url


def is_subdomain(domain):
    ext = tldextract.extract(domain)
    return bool(ext.subdomain)

def get_domain_from_subdomain(domain):
    ext = tldextract.extract(domain)
    return ext.registered_domain

