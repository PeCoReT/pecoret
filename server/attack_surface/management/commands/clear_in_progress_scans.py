from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from attack_surface.scanning.models.scan_batch import StatusChoices, ScanBatchRequest


class Command(BaseCommand):
    help = (
        "Deletes 'in progress' ScanBatchRequests with batch_start_time >= 5 days ago."
    )

    def handle(self, *args, **kwargs):
        cutoff_time = timezone.now() - timedelta(days=5)
        stale_scans = ScanBatchRequest.objects.filter(
            status=StatusChoices.IN_PROGRESS, batch_start_time__lte=cutoff_time
        )

        count = stale_scans.count()
        if count == 0:
            self.stdout.write(self.style.SUCCESS("No stale 'in progress' scans found."))
            return

        stale_scans.delete()
        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted {count} stale 'in progress' scan(s) older than 5 days."
            )
        )
