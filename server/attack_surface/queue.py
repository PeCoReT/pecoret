from django.conf import settings
from redis import Redis
from rq import Queue


def enqueue_scan(validated_data):
    if settings.AS_QUEUE.get('is_test'):
        # we are in unit test, not enqueue
        return
    queue_name = validated_data['scan_type']['name']
    redis = Redis(settings.AS_QUEUE['host'], int(settings.AS_QUEUE['port']))
    q = Queue(queue_name, connection=redis)
    # one day job timeout for large jobs
    job_id = q.enqueue('scanner.process_scan', args=(validated_data,), job_timeout=86400)
    # TODO: process job_id
    print(job_id)
