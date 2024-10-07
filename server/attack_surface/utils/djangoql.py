from pecoret.core.djangoql.schema import DjangoQLSchema


class PecoQLSchema(DjangoQLSchema):
    include = [
        'attack_surface.port',
        'attack_surface.program',
        'attack_surface.tag',
        'attack_surface.target',
        'attack_surface.url',
        'attack_surface.host',
        'attack_surface.asn',
        'attack_surface.service',
        'backend.technology',
    ]

