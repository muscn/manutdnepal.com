from rest_framework.permissions import BasePermission
from .models import DistributedKey


class DistributedKeyAuthentication(BasePermission):
    """
    Allows access only to requests with distributed key in header.
    """

    def has_permission(self, request, view):
        return request.META.get('HTTP_KEY') in DistributedKey.keys() or request.user.is_staff
