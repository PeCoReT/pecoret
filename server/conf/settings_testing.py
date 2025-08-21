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

REPORT_TEMPLATES = {
    'default_template': {
        'path': BASE_DIR / 'resources/report_templates/default_template/report_template.py'
    }
}

AS_ENABLE_SCANNING = True
