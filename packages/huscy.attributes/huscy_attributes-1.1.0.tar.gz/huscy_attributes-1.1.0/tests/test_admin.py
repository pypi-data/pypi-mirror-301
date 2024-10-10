import pytest

from django.contrib.admin.sites import AdminSite

from huscy.attributes import admin, models

pytestmark = pytest.mark.django_db


@pytest.fixture
def attribute_schema_admin():
    return admin.AttributeSchemaAdmin(model=models.AttributeSchema, admin_site=AdminSite())


@pytest.fixture
def attribute_set_admin():
    return admin.AttributeSetAdmin(model=models.AttributeSet, admin_site=AdminSite())


def test_attribute_schema_method_in_attribute_set_admin(attribute_set_admin, attribute_set):
    assert attribute_set_admin._attribute_schema(attribute_set) == attribute_set.attribute_schema.id


def test_has_add_permission_method_in_attribute_set_admin(attribute_set_admin):
    assert attribute_set_admin.has_add_permission(request=None) is False


def test_has_change_permission_method_in_attribute_set_admin(attribute_set_admin):
    assert attribute_set_admin.has_change_permission(request=None) is False


def test_has_delete_permission_method_in_attribute_schema_admin(attribute_schema_admin):
    assert attribute_schema_admin.has_delete_permission(request=None) is False
