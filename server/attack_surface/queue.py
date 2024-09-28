from django.conf import settings
from redis import Redis
from rq import Queue


def enqueue_scan(validated_data, depends_on=None):
    if settings.AS_QUEUE.get('is_test'):
        # we are in unit test, not enqueue for now
        return
    scan_type_name = validated_data['scan_type']['name']
    queue_name = settings.AS_QUEUE.get('queues', {}).get(scan_type_name, 'scanning')
    redis = Redis(settings.AS_QUEUE['host'], int(settings.AS_QUEUE['port']))
    q = Queue(queue_name, connection=redis)
    # one day job timeout for large jobs
    job = q.enqueue('scanner.process_scan', args=(validated_data, False), job_timeout=86400, depends_on=depends_on)
    # TODO: connect job_id to scan
    print(job)
    return job
