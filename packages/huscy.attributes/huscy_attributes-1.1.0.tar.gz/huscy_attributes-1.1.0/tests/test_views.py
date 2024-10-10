import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework.test import APIClient

from huscy.attributes.models import AttributeSet


pytestmark = pytest.mark.django_db


scenarios('features')


''' ============================================================================================ '''
'''                                      GIVEN                                                   '''
''' ============================================================================================ '''


@given('I am admin user', target_fixture='client')
def admin_user_client(admin_user):
    client = APIClient()
    client.login(username=admin_user.username, password='password')
    return client


@given('I am staff user', target_fixture='client')
def staff_user_client(staff_user):
    client = APIClient()
    client.login(username=staff_user.username, password='password')
    return client


@given('I am normal user', target_fixture='client')
def user_client(user):
    client = APIClient()
    client.login(username=user.username, password='password')
    return client


@given('I am anonymous user', target_fixture='client')
def anonymous_client():
    return APIClient()


@given(parsers.parse('I have {codename} permission'), target_fixture='codename')
def assign_permission(user, codename):
    permission = Permission.objects.get(codename=codename)
    user.user_permissions.add(permission)


@given('The latest attribute schema is in version 4')
def latest_attribute_schema(attribute_schema_v4):
    return attribute_schema_v4


@given('There\'s one attribute set with attribute schema version 2')
def attribute_set_with_schema_version_2(attribute_schema_v2, pseudonym):
    return AttributeSet.objects.create(
        pseudonym=pseudonym.code,
        attributes={
            'attribute1': 'any string',
        },
        attribute_schema=attribute_schema_v2,
    )


@given('There\'s one attribute set with attribute schema version 4')
def attribute_set_with_schema_version_4(attribute_set):
    return attribute_set


''' ============================================================================================ '''
'''                                      WHEN                                                    '''
''' ============================================================================================ '''


@when('I try to migrate an attribute set to latest attribute schema version',
      target_fixture='request_result')
def migrate_attribute_set_to_latest_schema_version(client, subject):
    return client.put(
        reverse('migrate-attributeset', kwargs=dict(subject_pk=subject.pk)),
    )


@when('I try to migrate an attribute set to attribute schema version 3',
      target_fixture='request_result')
def migrate_attribute_set_to_attribute_schema_version_3(client, subject, attribute_schema_v3):
    return client.put(
        reverse('migrate-attributeset', kwargs=dict(subject_pk=subject.pk)),
        data=dict(
            attribute_schema=attribute_schema_v3.id,
        ),
    )


@when('I try to migrate an attribute set to attribute schema version 3 and update attributes',
      target_fixture='request_result')
def migrate_attribute_set_to_attribute_schema_version_3_and_update_attributes(client, subject,
                                                                              attribute_schema_v3):
    return client.put(
        reverse('migrate-attributeset', kwargs=dict(subject_pk=subject.pk)),
        data=dict(
            attribute_schema=attribute_schema_v3.id,
            attributes={
                'attribute1': 'any string',
                'attribute2': 4.5,
            },
        ),
        format='json',
    )


@when('I try to migrate an attribute set to latest attribute schema version and update attributes',
      target_fixture='request_result')
def migrate_attribute_set_to_attribute_schema_version_4_and_update_attributes(client, subject):
    return client.put(
        reverse('migrate-attributeset', kwargs=dict(subject_pk=subject.pk)),
        data=dict(
            attributes={
                'attribute1': 'any string',
                'attribute2': 4.5,
                'category2': {
                    'attribute21': 100,
                    'attribute22': 'foobar',
                },
            },
        ),
        format='json',
    )


@when('I try to retrieve an attribute schema', target_fixture='request_result')
def retrieve_attribute_schema(client):
    return client.get(reverse('attributeschema'))


@when('I try to retrieve an attribute set', target_fixture='request_result')
def retrieve_attribute_set(client, subject):
    return client.get(reverse('attributeset', kwargs=dict(subject_pk=subject.id)))


@when('I try to update an attribute schema', target_fixture='request_result')
def update_attribute_schema(client):
    return client.put(
        reverse('attributeschema'),
        data={'schema': {'type': 'object', 'properties': {}}},
        format='json',
    )


@when('I try to update an attribute set', target_fixture='request_result')
def update_attribute_set(client, subject):
    return client.put(
        reverse('attributeset', kwargs=dict(subject_pk=subject.pk)),
        data=dict(
            attributes={
                'attribute1': 'another string',
                'attribute2': 1.0,
            },
        ),
        format='json'
    )


@when('I try to update attributes within attribute category 2', target_fixture='request_result')
def update_attribute_set_categories(client, subject):
    return client.put(
        reverse('attributeset', kwargs=dict(subject_pk=subject.pk)),
        data=dict(
            attributes={
                'attribute2': 1.0,
                'category2': {
                    'attribute21': 100,
                    'attribute22': 'foobar',
                },

            },
        ),
        format='json'
    )


''' ============================================================================================ '''
'''                                      THEN                                                    '''
''' ============================================================================================ '''


@then('I can see the non-categorized attributes')
def assert_non_categorized_attributes_visible(request_result):
    result = request_result.json()
    assert 'attribute1' in result['attributes']
    assert 'attribute2' in result['attributes']


@then('I cannot see category 1 attributes')
def assert_category_1_not_visible(request_result):
    result = request_result.json()
    assert 'category1' not in result['attributes']


@then('I cannot see category 2 attributes')
def assert_category_2_not_visible(request_result):
    result = request_result.json()
    assert 'category2' not in result['attributes']


@then('I can see category 1 attributes')
def assert_category_1_attributes_visible(request_result):
    result = request_result.json()
    assert 'category1' in result['attributes']
    assert 'attribute11' in result['attributes']['category1']


@then(parsers.parse('I get status code {status_code:d}'))
def assert_status_code(request_result, status_code):
    assert request_result.status_code == status_code, request_result.json()


@then(parsers.parse('The attribute schema version of the attribute set is in version 2'))
def assert_attribute_schema_version_is_in_version_2(schema_v2):
    assert AttributeSet.objects.get().attribute_schema.schema == schema_v2


@then(parsers.parse('The attribute schema version of the attribute set is in version 3'))
def assert_attribute_schema_version_is_in_version_3(schema_v3):
    assert AttributeSet.objects.get().attribute_schema.schema == schema_v3


@then(parsers.parse('The attribute schema version of the attribute set is in version 4'))
def assert_attribute_schema_version_is_in_version_4(schema_v4):
    assert AttributeSet.objects.get().attribute_schema.schema == schema_v4


@then('The attributes were updated to version 3')
def assert_attributes_updated_to_version_3():
    assert AttributeSet.objects.get().attributes == {
        'attribute1': 'any string',
        'attribute2': 4.5,
    }


@then('The attributes were updated to version 4')
def assert_attributes_updated_to_version_4():
    assert AttributeSet.objects.get().attributes == {
        'attribute1': 'any string',
        'attribute2': 4.5,
        'category2': {
            'attribute21': 100,
            'attribute22': 'foobar',
        },
    }
