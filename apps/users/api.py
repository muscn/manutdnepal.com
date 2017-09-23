import datetime
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from apps.key.permissions import DistributedKeyAuthentication
from apps.stats.serializers import FixtureSerializer
from apps.users.models import User, Membership
from apps.users.serializers import UserSerializer, MembershipSerializer


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # permission_classes = (DistributedKeyAuthentication,)

    def create(self, request):
        params = request.data
        # username = params.get('username')
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


class MembershipViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = MembershipSerializer
    queryset = Membership.objects.all()

    # permission_classes = (DistributedKeyAuthentication,)

    def create(self, request):
        params = request.data
        if not request.user.is_authenticated():
            return Response({'error': 'Provide user credential.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            item = request.user.membership
        except Membership.DoesNotExist:
            item = Membership(user=request.user)
        accounts = sorted(request.user.socialaccount_set.all(), key=lambda x: x.provider, reverse=True)
        for account in accounts:
            if account.provider == 'facebook':
                extra_data = account.extra_data
                try:
                    item.gender = extra_data['gender'][:1].upper()
                except KeyError:
                    pass
                try:
                    item.date_of_birth = datetime.datetime.strptime(extra_data['birthday'], '%m/%d/%Y').strftime(
                        '%Y-%m-%d')
                except KeyError:
                    pass
                try:
                    item.temporary_address = extra_data['location']['name']
                except KeyError:
                    pass
                try:
                    item.permanent_address = extra_data['hometown']['name']
                except KeyError:
                    pass
        try:
            item.user.full_name = params.get('full_name')
            item.user.save()
            item.date_of_birth = params.get('date_of_birth')
            # item.gender = params.get('gender')
            item.permanent_address = params.get('address')
            item.mobile = params.get('mobile')
            # item.identification_file = params.get('identification_file')
            item.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(MembershipSerializer(item).data, status=status.HTTP_200_OK)


class CustomObtainAuth(ObtainAuthToken):
    # permission_classes = (DistributedKeyAuthentication,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'status': user.status})
