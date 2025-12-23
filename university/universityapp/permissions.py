from rest_framework import permissions

class IsAdministrator(permissions.BasePermission):
    """Allow writes only for users with an Administrator profile or staff/superuser."""

    def has_permission(self, request, view):
        # Allow safe methods for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        # For unsafe methods, require admin profile or staff/superuser
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        # Check related Administrator profile
        return hasattr(user, 'administrator')
