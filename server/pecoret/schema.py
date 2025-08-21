from drf_spectacular.contrib.django_filters import DjangoFilterExtension
from drf_spectacular.extensions import OpenApiSerializerFieldExtension
from drf_spectacular.plumbing import append_meta
from drf_spectacular.plumbing import build_basic_type, build_object_type
from drf_spectacular.types import OpenApiTypes


class ValuedChoiceFieldFix(OpenApiSerializerFieldExtension):
    """fix for our `ValuedChoiceField`
    """

    target_class = "pecoret.core.serializers.ValuedChoiceField"

    def map_serializer_field(self, auto_schema, direction):
        return {"type": "string", "enum": self.target.choices.values()}


class PrimaryRelatedKeyFix(OpenApiSerializerFieldExtension):
    """fix for primary key related fields
    Source: https://drf-spectacular.readthedocs.io/en/latest/blueprints.html#drf-extra-fields-base64filefield
    """
    target_class = "pecoret.core.serializers.PrimaryKeyRelatedField"

    def map_serializer_field(self, auto_schema, direction):
        if direction == 'request':
            return build_basic_type(OpenApiTypes.INT)

        meta = auto_schema._get_serializer_field_meta(self.target, direction)
        schema = auto_schema.resolve_serializer(
            self.target.serializer(
                context=self.target.context, **self.target.serializer_kwargs,
            ),
            direction,
        ).ref
        return append_meta(schema, meta)


class CompanyScopedPrimaryRelatedKeyFix(PrimaryRelatedKeyFix):
    target_class = 'pecoret.core.serializers.CompanyScopedPrimaryKeyRelatedField'


class ReportAuthorRelatedFieldFix(PrimaryRelatedKeyFix):
    target_class = 'pecoret.core.serializers.ReportAuthorRelatedField'


class NonDraftAdvisoryPrimaryKeyRelatedField(PrimaryRelatedKeyFix):
    target_class = 'pecoret.core.serializers.NonDraftAdvisoryPrimaryKeyRelatedField'


class ProjectFilteredPrimaryKeyRelatedField(PrimaryRelatedKeyFix):
    target_class = 'pecoret.core.serializers.ProjectFilteredPrimaryKeyRelatedField'


class LabelFieldFix(PrimaryRelatedKeyFix):
    target_class = 'advisories.fields.label.LabelField'


class AssetGenericRelatedField(PrimaryRelatedKeyFix):
    target_class = 'pecoret.core.serializers.AssetGenericRelatedField'

    def map_serializer_field(self, auto_schema, direction):
        type_enum = []
        for serializer_key in self.target.serializers.keys():
            type_enum.append(serializer_key.asset_type)
        if direction == 'request':
            return build_object_type({
                'type': {'type': 'string', 'enum': type_enum},
                'pk': build_basic_type(OpenApiTypes.INT),
            })
        one_of_schemas = []
        for serializer_key, serializer in self.target.serializers.items():
            schema = auto_schema.resolve_serializer(
                serializer,
                direction,
            )
            one_of_schemas.append(schema.ref)
        return build_object_type({
            'type': {'type': 'string', 'enum': type_enum},
            'object': {'oneOf': one_of_schemas},
        })


class ValuedChoiceFilterFix(DjangoFilterExtension):
    """spectacular fix for custom ChoiceFilter"""

    target_class = "django_filters.rest_framework.DjangoFilterBackend"
    priority = 1
    match_subclasses = True

    def _get_explicit_filter_choices(self, filter_field):
        """override filter choices for values instead of key"""
        if "choices" not in filter_field.extra:
            return None
        if callable(filter_field.extra["choices"]):
            # choices function may utilize the DB, so refrain from actually calling it.
            return []
        else:
            # only use values as valid choice filters
            return [v for _, v in filter_field.extra["choices"]]
