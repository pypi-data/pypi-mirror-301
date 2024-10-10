from django.contrib import admin

from huscy.attributes import models, services


@admin.register(models.AttributeSchema)
class AttributeSchemaAdmin(admin.ModelAdmin):
    list_display = 'id', 'schema'

    def save_model(self, request, attribute_schema, form, change):
        services.update_attribute_schema(attribute_schema.schema)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.AttributeSet)
class AttributeSetAdmin(admin.ModelAdmin):
    list_display = 'pseudonym', '_attribute_schema', 'attributes'

    def _attribute_schema(self, attribute_set):
        return attribute_set.attribute_schema.id

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
