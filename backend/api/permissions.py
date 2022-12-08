from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrCreate(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method == 'POST'
            or (request.user and request.user.is_staff)
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or (request.user and request.user.is_staff)
        )
