from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from ..key.permissions import DistributedKeyAuthentication
from .models import UserDevice
from .serializers import UserDeviceSerializer


class UserDeviceViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserDeviceSerializer
    queryset = UserDevice.objects.all()
    permission_classes = (DistributedKeyAuthentication,)

    def create(self, request, *args, **kwargs):
        params = request.data
        try:
            obj, created = UserDevice.objects.get_or_create(dev_id=params.get('dev_id'))
            obj.name = params.get('name')
            obj.reg_id = params.get('reg_id')
            obj.device_type = params.get('type')
            # TODO UserDevice set User
            # obj.user = request.user
            obj.is_active = True
            obj.save()
            return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)