from pecoret.settings import *

Q_CLUSTER = {
    "name": "DjangORM",
    "attempt_count": 1,
    "max_attempts": 1,
    "ack_failures": True,
    "bulk": 1,
    "retry": 900,
    "timeout": 600,
    "orm": "default",
    "sync": True
}

