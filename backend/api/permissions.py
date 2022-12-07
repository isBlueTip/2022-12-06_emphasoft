from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAdminUser)


class IsAuthenticatedOrReadOnlyOrRegister(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method == "POST"
            or request.method == SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )


class IsAdminOrCreate(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (request.user and request.user.is_authenticated)
        )


# class IsAuthor(BasePermission):
#     def has_permission(self, request, view):
#         print(1)
#         return bool(
#             # request.method == SAFE_METHODS
#             request.user and request.user.is_authenticated
#         )
#
#     def has_object_permission(self, request, view, obj):
#         return bool(obj.guest == request.user)


class IsAdminOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or (request.user and request.user.is_staff)
        )
