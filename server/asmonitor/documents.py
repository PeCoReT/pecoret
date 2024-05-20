from django_opensearch_dsl import Document, fields
from django_opensearch_dsl.registries import registry
from .models.target import Target


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

    class Index:
        name = 'targets'
        auto_refresh = True

    class Django:
        model = Target
        fields = [
            'id', 'date_created', 'date_updated', 'scope', 'last_seen', 'description', 'name'
        ]
