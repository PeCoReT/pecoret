from django_opensearch_dsl import Document, fields
from django_opensearch_dsl.registries import registry

from .models.target import Target
from .models.url import URL
from .models.finding import Finding


@registry.register_document
class TargetDocument(Document):
    technologies = fields.ObjectField(properties={
        'name': fields.TextField(),
        'cpe': fields.TextField(),
        'description': fields.TextField(),
        'vendor': fields.TextField()
    })
    tags = fields.ObjectField(properties={
        'name': fields.TextField(),
        'description': fields.TextField()
    })
    program = fields.ObjectField(properties={
        'name': fields.TextField()
    })
    ip = fields.IpField()
    ports = fields.NestedField(attr='port_set', properties={
        'protocol': fields.TextField(attr='get_protocol_display'),
        'port': fields.IntegerField(),
        'service': fields.TextField(),
        'banner': fields.TextField()
    })

    class Index:
        name = 'peco-targets'
        auto_refresh = True

    class Django:
        model = Target
        fields = [
            'id', 'date_created', 'date_updated', 'scope', 'last_seen', 'description', 'name'
        ]


@registry.register_document
class URLDocument(Document):
    target = fields.NestedField(properties={
        'ip': fields.TextField(), 'name': fields.TextField(),
        'technologies': fields.ObjectField(properties={
            'name': fields.TextField(),
            'cpe': fields.TextField(),
            'description': fields.TextField(),
            'vendor': fields.TextField()
        })
    })

    class Django:
        model = URL
        fields = [
            'last_seen', 'status_code', 'request', 'response', 'date_updated', 'date_created'
        ]

    class Index:
        name = 'peco-urls'
        auto_refresh = True


@registry.register_document
class FindingDocument(Document):
    target = fields.NestedField(properties={
        'ip': fields.TextField(), 'name': fields.TextField(),
    })
    status = fields.TextField(attr='get_status_display')

    program = fields.ObjectField(properties={
        'name': fields.TextField()
    })
    severity = fields.TextField(attr='get_severity_display')
    tags = fields.ObjectField(properties={
        'name': fields.TextField(),
        'description': fields.TextField()
    })

    class Django:
        model = Finding
        fields = [
            'id', 'description', 'internal_information', 'recommendation', 'proof_text', 'date_created',
            'date_updated', 'name'
        ]

    class Index:
        name = 'peco-findings'
        auto_refresh = True
