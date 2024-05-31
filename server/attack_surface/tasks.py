from attack_surface.utils.technology import get_nested_technologies
from attack_surface.models import URL


def sync_implicit_techs_url(url_pk):
    """
    sync implicit technologies to the URL instance
    """
    try:
        url = URL.objects.get(pk=url_pk)
    except URL.DoesNotExist:
        # url seems to be removed in the meantime
        return

    technologies = get_nested_technologies(url)
    for tech in technologies:
        url.technologies.add(tech)
    url.save()
