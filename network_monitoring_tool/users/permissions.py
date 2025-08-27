from rest_framework.permissions import BasePermission, SAFE_METHODS
from .constants import ROLE_ADMIN, ROLE_EDITOR, ROLE_VIEWER


class IsAdmin(BasePermission):
    """Allow only Admin role"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role
            and request.user.role.name == ROLE_ADMIN
        )


class IsEditorOrAdmin(BasePermission):
    """Allow Editor and Admin roles"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role
            and request.user.role.name in [ROLE_ADMIN, ROLE_EDITOR]
        )


class IsViewerOrReadOnly(BasePermission):
    """Allow read-only for Viewer, full for Admin/Editor"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated or not request.user.role:
            return False

        role_name = request.user.role.name

        if role_name == ROLE_VIEWER:
            return request.method in SAFE_METHODS
        return role_name in [ROLE_ADMIN, ROLE_EDITOR]


class RolePermission(BasePermission):
    """
    Generic role permission class.
    Allows defining which roles have full access
    and which roles are read-only.
    """

    def __init__(self, allowed_roles=None, read_only_roles=None):
        self.allowed_roles = allowed_roles or []
        self.read_only_roles = read_only_roles or []

    def has_permission(self, request, view):
        if not request.user.is_authenticated or not request.user.role:
            return False

        role_name = request.user.role.name

        if role_name in self.allowed_roles:
            return True

        if role_name in self.read_only_roles:
            return request.method in SAFE_METHODS

        return False
