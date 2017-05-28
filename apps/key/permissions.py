from rest_framework.permissions import BasePermission
from .models import DistributedKey


class DistributedKeyAuthentication(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        try:
            DistributedKey.objects.get(key=request.META.get('HTTP_KEY'))
            return True
        except DistributedKeyAuthentication.DoesNotExist as e:
            return False