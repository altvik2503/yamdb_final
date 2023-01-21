from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Администратор."""

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Администратор или только для чтения."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
        )


class IsAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    """Администратор, модератор, автор или только для чтения."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )
