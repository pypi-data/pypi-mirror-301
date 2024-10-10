from rest_framework.permissions import BasePermission, SAFE_METHODS


class MigrateAttributeSetPermission(BasePermission):
    def has_permission(self, request, view):
        return all([
            request.method == 'PUT',
            request.user.has_perm('attributes.migrate_attributeset'),
        ])


class RetrieveAttributeSetPermission(BasePermission):
    def has_permission(self, request, view):
        return all([
            request.method == 'GET',
            request.user.has_perm('attributes.view_attributeset'),
        ])


class UpdateAttributeSetPermission(BasePermission):
    def has_permission(self, request, view):
        return all([
            request.method == 'PUT',
            request.user.has_perms(['subjects.change_subject', 'attributes.change_attributeset'])
        ])


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in SAFE_METHODS
