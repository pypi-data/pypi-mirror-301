from django.shortcuts import get_object_or_404
from rest_framework.generics import RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response

from huscy.attributes import serializer, services
from huscy.attributes.models import AttributeSchema, AttributeSet
from huscy.attributes.permissions import (
    MigrateAttributeSetPermission,
    ReadOnly,
    RetrieveAttributeSetPermission,
    UpdateAttributeSetPermission,
)
from huscy.subjects.models import Subject


class AttributeSchemaView(RetrieveUpdateAPIView):
    permission_classes = (DjangoModelPermissions | ReadOnly, )
    queryset = AttributeSchema.objects.all()
    serializer_class = serializer.AttributeSchemaSerializer

    def get_object(self):
        attribute_schema = services.get_attribute_schema()
        return services.resolve_attribute_schema_refs(attribute_schema)


class BaseAttributeSetView:

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.subject = get_object_or_404(Subject, pk=self.kwargs['subject_pk'])

    def get_object(self):
        return services.get_attribute_set(self.subject)


class AttributeSetView(BaseAttributeSetView, RetrieveUpdateAPIView):
    permission_classes = (
        IsAuthenticated,
        RetrieveAttributeSetPermission | UpdateAttributeSetPermission
    )
    serializer_class = serializer.AttributeSetSerializer

    def update(self, request, *args, **kwargs):
        attribute_set = self.get_object()

        serializer = self.get_serializer(attribute_set, data=request.data)
        serializer.is_valid(raise_exception=True)

        for node, node_description in attribute_set.attribute_schema.schema['properties'].items():
            if (node in serializer.validated_data['attributes'] and
                    node_description.get('type', None) == 'object' and
                    not self.request.user.has_perm(f'attributes.change_attribute_category_{node}')):
                raise PermissionDenied('You don\'t have the permission to update attribute '
                                       f'category {node}')

        self.perform_update(serializer)

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        attribute_set = self.get_object()

        for node, node_description in attribute_set.attribute_schema.schema['properties'].items():
            if all([node_description.get('type', None) == 'object',
                    node in attribute_set.attributes,
                    not request.user.has_perm(f'attributes.view_attribute_category_{node}')]):
                attribute_set.attributes.pop(node)

        serializer = self.get_serializer(attribute_set)
        return Response(serializer.data)


class MigrateAttributeSetView(BaseAttributeSetView, UpdateAPIView):
    permission_classes = IsAuthenticated, MigrateAttributeSetPermission
    queryset = AttributeSet.objects.none()
    serializer_class = serializer.MigrateAttributeSetSerializer
