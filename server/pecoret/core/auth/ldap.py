from django.contrib.auth.models import Group
from django.conf import settings


def sync_ldap_groups(user):
    """
    get a mapping of our groups to custom LDAP groups which is not yet (?) supported in django-auth-ldap
    https://github.com/django-auth-ldap/django-auth-ldap/issues/125
    """
    if not settings.LDAP_SYNC_GROUP_MAPPING:
        return
    if user.ldap_user._groups._group_infos:
        for ldap_group, _instance in user.ldap_user._groups._group_infos:
            mapping = settings.LDAP_SYNC_GROUP_MAPPING.get(ldap_group)
            if not mapping:
                continue
            group = Group.objects.filter(name=mapping)
            # invalid group used in mapping which does not exist in PeCoReT, skipping
            if not group.exists():
                continue
            group = group.get()
            user.groups.add(group)
        # remove groups from user which are not part of the LDAP
        diff = user.groups.difference(Group.objects.filter(name__in=user.ldap_user.group_names))
        for item in diff:
            user.groups.remove(item)
    else:
        # no groups. wipe all group user
        user.groups.remove(Group.objects.filter(name__in=list(settings.LDAP_SYNC_GROUP_MAPPING.values())))
    user.save()
