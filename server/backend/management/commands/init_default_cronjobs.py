from django.core.management.base import BaseCommand
from django_q.tasks import Schedule


class Command(BaseCommand):
    help = "Create some default cronjobs"

    def handle(self, *args, **options):
        self.init_check_project_membership_expiry()

    def init_check_project_membership_expiry(self):
        func_name = "backend.tasks.memberships.check_project_membership_expiry"
        if not Schedule.objects.filter(func=func_name).exists():
            Schedule.objects.create(func=func_name, schedule_type=Schedule.DAILY)
