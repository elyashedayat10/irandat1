from rest_framework.permissions import BasePermission


class ActiveUserPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_active