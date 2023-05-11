
from rest_framework.permissions import BasePermission

class NotAuthenticated(BasePermission):
    message="You already have account."

    def has_permission(self, request, view):   # burası her zaman çalışır.
        return not request.user.is_authenticated
