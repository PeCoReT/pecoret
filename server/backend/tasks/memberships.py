from django.utils import timezone
from backend.models.membership import Membership


def check_project_membership_expiry():
    now = timezone.now()
    qs = Membership.objects.filter(active_until__isnull=False, active_until__lte=now)
    qs.delete()
    return True
