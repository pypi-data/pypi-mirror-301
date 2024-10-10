from operator import attrgetter

import jsonschema
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.db.transaction import atomic

from huscy.attributes.models import AttributeSchema, AttributeSet
from huscy.pseudonyms.services import get_or_create_pseudonym


class AttributeSetMigrationError(Exception):
    pass


def get_attribute_schema(version=None):
    if version is None:
        return AttributeSchema.objects.latest('pk')
    else:
        return AttributeSchema.objects.get(pk=version)


def get_attribute_set(subject):
    pseudonym = get_or_create_pseudonym(subject, 'attributes.attributeset')
    return _get_or_create_attribute_set(pseudonym.code)


def _get_or_create_attribute_set(pseudonym):
    attribute_set, _created = AttributeSet.objects.select_related('attribute_schema').get_or_create(
        pseudonym=pseudonym,
        defaults=dict(
            attribute_schema=AttributeSchema.objects.latest('id'),
            attributes={},
        ),
    )
    return attribute_set


def migrate_attribute_set(attribute_set, attribute_schema=None, attributes=None):
    if attribute_schema is None:
        attribute_schema = AttributeSchema.objects.latest('id')

    if attribute_schema.pk <= attribute_set.attribute_schema.pk:
        raise AttributeSetMigrationError('New version for attribute schema must be greater than '
                                         'current attribute schema version.')

    attribute_set.attribute_schema = attribute_schema

    if attributes is not None:
        attribute_set.attributes = attributes

    jsonschema.validate(attribute_set.attributes, attribute_schema.schema)

    attribute_set.save()
    return attribute_set


def resolve_attribute_schema_refs(attribute_schema):
    defs = attribute_schema.schema.get('$defs', {})
    attribute_schema.schema = resolve_refs(attribute_schema.schema, defs)
    return attribute_schema


def resolve_refs(schema, defs):
    if not isinstance(schema, dict):
        return schema

    if '$ref' in schema:
        ref_path = schema['$ref'].split('/')
        ref_key = ref_path[-1]
        return resolve_refs(defs[ref_key], defs)
    else:
        return {key: resolve_refs(value, defs) for key, value in schema.items()}


@atomic
def update_attribute_schema(schema):
    attribute_schema = AttributeSchema.objects.create(schema=schema)
    created_permissions = _create_attribute_category_permissions(schema)
    _delete_orphaned_attribute_category_permissions(created_permissions)
    return attribute_schema


def _create_attribute_category_permissions(schema):
    content_type = ContentType.objects.get_for_model(AttributeSchema)

    permissions = []
    for name, value in schema['properties'].items():
        if value.get('type', None) == 'object':
            permissions.append(_create_attribute_category_read_permission(content_type, name))
            permissions.append(_create_attribute_category_write_permission(content_type, name))
    return permissions


def _create_attribute_category_read_permission(content_type, attribute_category_name):
    permission, created = Permission.objects.get_or_create(
        codename=f'view_attribute_category_{attribute_category_name}',
        name=f'Can view attribute category {attribute_category_name}',
        content_type=content_type
    )
    return permission


def _create_attribute_category_write_permission(content_type, attribute_category_name):
    permission, created = Permission.objects.get_or_create(
        codename=f'change_attribute_category_{attribute_category_name}',
        name=f'Can change attribute category {attribute_category_name}',
        content_type=content_type
    )
    return permission


def _delete_orphaned_attribute_category_permissions(created_permissions):
    queryset = Permission.objects
    queryset = queryset.filter(Q(codename__startswith='change_attribute_category_') |
                               Q(codename__startswith='view_attribute_category_'))
    queryset = queryset.exclude(codename__in=map(attrgetter('codename'), created_permissions))
    queryset.delete()


def update_attribute_set(attribute_set, attributes):
    _dict_merge(attribute_set.attributes, attributes)
    jsonschema.validate(attribute_set.attributes, attribute_set.attribute_schema.schema)
    attribute_set.save(update_fields=['attributes'])
    return attribute_set


def _dict_merge(source_dict, merge_dict):
    for key, value in merge_dict.items():
        if key in source_dict and isinstance(source_dict[key], dict) and isinstance(value, dict):
            _dict_merge(source_dict[key], value)
        else:
            source_dict[key] = value
