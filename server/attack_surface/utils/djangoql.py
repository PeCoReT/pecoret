from pecoret.core.djangoql.schema import DjangoQLSchema


class PecoQLSchema(DjangoQLSchema):
    include = [
        'attack_surface.program',
        'attack_surface.tag',
        'attack_surface.target',
        'attack_surface.url',
        'attack_surface.asn',
        'attack_surface.service',
        'backend.technology',
    ]
