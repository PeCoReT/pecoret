from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from attack_surface.scanning.models.scan_batch import StatusChoices, ScanBatchRequest


class Command(BaseCommand):
    help = (
        "Deletes ScanBatchRequest records older than one month based on date_created."
    )

    def handle(self, *args, **kwargs):
        cutoff_date = timezone.now() - timedelta(days=30)
        old_batches = ScanBatchRequest.objects.filter(
            date_created__lt=cutoff_date, status=StatusChoices.COMPLETED
        )

        count = old_batches.count()
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS("No old scan batches found to delete.")
            )
            return

        old_batches.delete()
        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted {count} ScanBatchRequest record(s) older than one month."
            )
        )
