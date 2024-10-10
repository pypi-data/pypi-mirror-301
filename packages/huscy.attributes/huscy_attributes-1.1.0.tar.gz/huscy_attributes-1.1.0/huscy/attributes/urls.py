from django.urls import path

from . import views


urlpatterns = [
    path(
        'api/attributeschema/',
        views.AttributeSchemaView.as_view(),
        name='attributeschema',
    ),
    path(
        'api/subjects/<uuid:subject_pk>/attributeset/migrate/',
        views.MigrateAttributeSetView.as_view(),
        name='migrate-attributeset',
    ),
    path(
        'api/subjects/<uuid:subject_pk>/attributeset/',
        views.AttributeSetView.as_view(),
        name='attributeset',
    ),
]
