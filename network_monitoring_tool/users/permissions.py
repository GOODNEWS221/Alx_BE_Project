from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    """Allow only Admin role"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role and request.user.role.name == "Admin"


class IsEditorOrAdmin(BasePermission):
    """Allow Editor and Admin roles"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role and 
            request.user.role.name in ["Admin", "Editor"]
        )


class IsViewerOrReadOnly(BasePermission):
    """Allow read-only for Viewer, full for Admin/Editor"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated or not request.user.role:
            return False
        if request.user.role.name == "Viewer":
            return request.method in SAFE_METHODS
        return True