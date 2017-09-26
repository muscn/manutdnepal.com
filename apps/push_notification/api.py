from django.db import IntegrityError
from rest_framework import viewsets, mixins
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status
from ..key.permissions import DistributedKeyAuthentication
from .models import UserDevice
from .serializers import UserDeviceSerializer


class UserDeviceViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserDeviceSerializer
    queryset = UserDevice.objects.all()

    def create(self, request, *args, **kwargs):
        params = request.data
        user = request.user if request.user.is_authenticated else None
        reg_id = params.get('reg_id')
        if reg_id and reg_id.lower() != 'blacklisted':
            obj, created = UserDevice.objects.update_or_create(dev_id=params.get('dev_id'),
                                                               defaults={'name': params.get('name'), 'reg_id': reg_id,
                                                                         'device_type': params.get('type'), 'is_active': True,
                                                                         'user': user})
            return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)
        else:
            raise APIException('No registration ID.')
