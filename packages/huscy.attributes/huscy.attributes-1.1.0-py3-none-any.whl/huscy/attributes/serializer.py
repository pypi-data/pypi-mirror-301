from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from huscy.attributes import models, services


class AttributeSchemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttributeSchema
        fields = (
            'id',
            'created_at',
            'schema',
        )

    def create(self, validated_data):
        return services.update_attribute_schema(**validated_data)


class AttributeSetSerializer(serializers.ModelSerializer):
    attribute_schema = AttributeSchemaSerializer(read_only=True)

    class Meta:
        model = models.AttributeSet
        fields = (
            'attribute_schema',
            'attributes',
        )

    def update(self, attribute_set, validated_data):
        return services.update_attribute_set(attribute_set, **validated_data)


class MigrateAttributeSetSerializer(serializers.ModelSerializer):
    attribute_schema = serializers.PrimaryKeyRelatedField(
        queryset=models.AttributeSchema.objects.all(),
        required=False,
    )
    attributes = serializers.JSONField(required=False)

    class Meta:
        model = models.AttributeSet
        fields = (
            'attribute_schema',
            'attributes',
        )

    def update(self, attribute_set, validated_data):
        try:
            return services.migrate_attribute_set(attribute_set, **validated_data)
        except services.AttributeSetMigrationError as e:
            raise ValidationError(str(e))
