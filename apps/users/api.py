import datetime
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from apps.key.permissions import DistributedKeyAuthentication
from apps.stats.serializers import FixtureSerializer
from apps.users.models import User, Membership, MembershipSetting
from apps.users.serializers import UserSerializer, MembershipSerializer


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = []

    def list(self, request):
        if self.request.user.is_authenticated:
            data = UserSerializer(self.request.user, many=False).data
            data['membership_fee'] = MembershipSetting.get_solo().membership_fee
            return Response(data)
        return Response({'status': 'error', 'detail': 'Not authenticated.'}, 401)

    def create(self, request):
        params = request.data
        email = params.get('email')
        password = params.get('password')
        full_name = params.get('full_name')
        try:
            user = User.objects.create_user(email, password)
            user.full_name = full_name
            user.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)


class CustomObtainAuth(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'status': user.status})
