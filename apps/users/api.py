import datetime
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import list_route
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from apps.key.permissions import DistributedKeyAuthentication
from apps.payment.models import Payment, ReceiptData, DirectPayment, BankDeposit, BankAccount
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

    def create(self, request, *args, **kwargs):
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

    @list_route(methods=['POST'])
    def membership(self, request):
        user = request.user
        if not user.is_authenticated:
            raise APIException('You need to login first.')
        data = request.data
        if user.status == 'Pending Approval':
            raise APIException('Your membership request in pending approval.')
        if user.status == 'Member':
            raise APIException('You are already a member.')
        membership_setting = MembershipSetting.get_solo()
        if not data.get('full_name'):
            raise APIException('Full name is required.')
        if not data.get('mobile'):
            raise APIException('Mobile number is required.')
        payment_type = 'Renewal' if user.status == 'Expired' else 'Membership'
        payment = Payment(user=user, amount=float(membership_setting.membership_fee), type=payment_type)
        # todo api check esewa
        if data.get('esewa'):
            pass
        elif data.get('receipt'):
            receipt_no = data.get('receipt_no')
            if not receipt_no:
                raise APIException('Receipt number is required.')
            elif not receipt_no.isdigit():
                raise APIException('Invalid receipt number.')
            elif not ReceiptData.objects.filter(active=True, from_no__lte=receipt_no, to_no__gte=receipt_no).exists():
                raise APIException('Invalid receipt number.')
            elif DirectPayment.objects.filter(receipt_no=receipt_no, payment__verified_by__isnull=False).exists():
                raise APIException('Invalid receipt number.')
            else:
                payment.save()
                DirectPayment.objects.create(payment=payment, receipt_no=receipt_no)
        elif data.get('deposit'):
            if not request.FILES.get('voucher_image'):
                raise APIException('Voucher image is required.')
            else:
                payment.save()
                BankDeposit.objects.create(payment=payment, voucher_image=request.FILES.get('voucher_image'),
                                           bank=BankAccount.objects.first())
        else:
            raise APIException('No payment method specified.')
        user.status = 'Pending Approval'
        user.save()
        data = UserSerializer(user, many=False).data
        return Response(data)


class CustomObtainAuth(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(self.request.user, many=False).data
        user_data['token'] = token.key
        return Response(user_data)
