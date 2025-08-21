from drf_spectacular.utils import extend_schema, extend_schema_view


def extend_viewset_schema(tags, verbose_name, verbose_name_plural=None):
    if verbose_name_plural is None:
        verbose_name_plural = f'{verbose_name}s'

    def decorator(viewset_class):
        return extend_schema_view(
            list=extend_schema(
                tags=tags,
                operation_id=f'Get all {verbose_name_plural}'
            ),
            retrieve=extend_schema(
                tags=tags,
                operation_id=f'Get a specific {verbose_name}'
            ),
            destroy=extend_schema(
                tags=tags,
                operation_id=f'Delete a {verbose_name}'
            ),
            create=extend_schema(
                tags=tags,
                operation_id=f'Create a {verbose_name}'
            ),
            update=extend_schema(
                tags=tags,
                operation_id=f'Update a {verbose_name}'
            ),
            partial_update=extend_schema(
                tags=tags,
                operation_id=f'Partial update a {verbose_name}'
            )
        )(viewset_class)
    return decorator
