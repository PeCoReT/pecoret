import time

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db.models import Min, Q
from django.utils import timezone

from attack_surface import models
from attack_surface.models.scan import ScanStatus
from attack_surface.queue import enqueue_scan
from attack_surface.serializers.scanning.scan import ScanSerializer


class Command(BaseCommand):
    """ enqueue scans for all enabled scan types, when queue has less than 10 items and scan was not performed in last 6h"""
    # TODO: also check if scan was performed this day already
    queue_size = 10
    timediff = 6  # in hours

    def handle(self, *args, **options):
        scan_types = models.ScanType.objects.enabled()
        pending_scans = models.Scan.objects.filter(Q(status=ScanStatus.PENDING) | Q(status=ScanStatus.RUNNING))

        time_ago = timezone.now() - timezone.timedelta(hours=self.timediff)

        if pending_scans.count() >= 10:
            print("Queue already full!")
            return
        for scan_type in scan_types:
            Model = apps.get_model(f'attack_surface.{scan_type.allowed_object_type}')
            objs = list(Model.objects.annotate(last_scan=Min('scan_objects__scan__date_created')).filter(
                (Q(scan_objects__scan__scan_type=scan_type) | Q(last_scan__isnull=True)) & (
                        Q(last_scan__lt=time_ago) | Q(last_scan__isnull=True))).order_by('last_scan').distinct())[:5]
            if not objs:
                continue
            scan_name = f'CS-{scan_type.name}-{str(int(time.time()))}'
            scan = models.Scan.objects.create(name=scan_name, scan_type=scan_type)
            for obj in objs:
                ct = ContentType.objects.get_for_model(obj)
                models.ScanObject.objects.get_or_create(scan=scan, content_type=ct, object_id=obj.pk)
            serializer = ScanSerializer(instance=scan)
            print(serializer.data)
            enqueue_scan(serializer.data)
