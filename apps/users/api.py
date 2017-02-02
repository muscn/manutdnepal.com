from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from apps.key.permissions import DistributedKeyAuthentication
from apps.stats.serializers import FixtureSerializer
from apps.users.models import User
from apps.users.serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (DistributedKeyAuthentication,)

    def create(self, request):
        params = request.data
        username = params.get('username')
        email = params.get('email')
        password = params.get('password')
        full_name = params.get('full_name')
        try:
            user = User.objects.create_user(username, email, password)
            user.full_name = full_name
            user.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)