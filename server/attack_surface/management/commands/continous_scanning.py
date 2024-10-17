import time

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import Min, Q
from django.utils import timezone

from attack_surface import models
from attack_surface.models.scan import ScanStatus
from attack_surface.serializers.scanning.scan import ScanSerializer


class Command(BaseCommand):
    """ enqueue scans for all enabled scan types, when queue has less than 10 items and scan was not performed in last 6h"""

    def add_arguments(self, parser):
        # Adding optional arguments
        parser.add_argument(
            '--scan_type_name',
            type=str,
            default=None,
            help='Optional scan type name to filter the scan types.',
        )
        parser.add_argument(
            '--queue_size',
            type=int,
            default=10,
            help=f'Queue size limit (default: 10)',
        )
        parser.add_argument(
            '--timediff',
            type=int,
            default=6,
            help=f'Time difference in hours (default: 6)',
        )


    def handle(self, *args, **options):
        scan_types = models.ScanType.objects.enabled()
        if options.get('scan_type_name'):
            scan_types = scan_types.filter(name=options['scan_type_name'])
        pending_scans = models.Scan.objects.filter(Q(status=ScanStatus.PENDING) | Q(status=ScanStatus.RUNNING))

        time_ago = timezone.now() - timezone.timedelta(hours=options['timediff'])

        if pending_scans.count() >= options['queue_size']:
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
            data = {'scan_objects': [], 'scan_type': scan_type.pk, 'name': scan_name}
            for obj in objs:
                if not obj.is_in_scope:
                    # not scan items that are not in scope
                    continue
                obj_data = {'content_type': obj._meta.model_name, 'object_id': obj.pk}
                data['scan_objects'].append(obj_data)
            if len(data['scan_objects']) < 1:
                # no scan objects - skipping
                continue
            serializer = ScanSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
