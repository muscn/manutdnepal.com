import json

from allauth.account.utils import setup_user_email, send_email_confirmation
from allauth.socialaccount.models import SocialToken
from django.db import IntegrityError
from rest_framework import mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import list_route, parser_classes
from rest_framework.exceptions import APIException
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from apps.partner.models import Partner
from apps.partner.serializers import PartnerSer
from apps.payment.models import Payment, ReceiptData, DirectPayment, BankDeposit, BankAccount, EsewaPayment
from apps.push_notification.models import UserDevice
from apps.users.models import User, MembershipSetting, CardStatus, SocialLoginToken
from apps.users.serializers import UserSerializer, AuthTokenSerializer
from muscn.utils.football import season


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request):
        if self.request.user.is_authenticated:
            data = UserSerializer(self.request.user, many=False).data
            return Response(data)
        return Response({'status': 'error', 'detail': 'Not authenticated.'}, 401)

    def create(self, request, *args, **kwargs):
        params = request.data
        email = params.get('email')
        password = params.get('password')
        full_name = params.get('full_name')
        try:
            user = User.objects.create_user(email, password, full_name=full_name, active=False)
            social_data = request.data.get('social')
            if social_data:
                try:
                    SocialLoginToken.create(user, social_data)
                except ValueError as e:
                    raise APIException(str(e))
            setup_user_email(request, user, [])
            send_email_confirmation(request, user, signup=True)
        except IntegrityError:
            return Response({'detail': 'The e-mail address already exists.'}, status=400)
        except Exception as e:
            return Response({'detail': str(e)}, status=400)
        return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)

    @list_route(methods=['GET', 'POST'])
    @parser_classes((FormParser, MultiPartParser,))
    def membership(self, request):
        if request.method == 'GET':
            if request.user.is_authenticated:
                data = UserSerializer(self.request.user, many=False).data
                data['membership_fee'] = MembershipSetting.get_solo().membership_fee
                data['pickup_locations'] = PartnerSer(Partner.objects.filter(pickup_location=True), many=True).data
                return Response(data)
            return Response({'status': 'error', 'detail': 'Not authenticated.'}, 401)
        if request.method == 'POST':
            user = request.user
            if not user.is_authenticated:
                return Response({'status': 'error', 'detail': 'Not authenticated.'}, 401)
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
            if not data.get('pickup_location'):
                raise APIException('Pickup Location is required')
            user.full_name = data.get('full_name')
            user.mobile = data.get('mobile')
            user.save()
            CardStatus.objects.update_or_create(user=user, season=season(), defaults={'status': 'Awaiting Approval',
                                                                                      'pickup_location_id': data.get(
                                                                                          'pickup_location')})
            payment_type = 'Renewal' if user.status == 'Expired' else 'Membership'
            payment = Payment(user=user, amount=float(membership_setting.membership_fee), type=payment_type)
            if data.get('esewa'):
                response = json.loads(data.get('esewa_response'))
                if float(response['totalAmount']) < float(payment.amount):
                    raise APIException('You did not pay the full amount.')
                esewa_payment = EsewaPayment(amount=payment.amount, pid=response['productId'],
                                             ref_id=response['transactionDetails']['referenceId'])
                if esewa_payment.verify():
                    payment.save()
                    esewa_payment.payment = payment
                    esewa_payment.get_details()
                    esewa_payment.save()
                else:
                    raise APIException('Payment via eSewa failed!')

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
                if not request.data.get('voucher_image'):
                    raise APIException('Voucher image is required.')
                else:
                    payment.save()
                    bd = BankDeposit.objects.create(payment=payment, voucher_image=request.data.get('voucher_image'),
                                                    bank=BankAccount.objects.first())
                    if not bd.voucher_image:
                        payment.delete()
                        raise APIException('Could not save voucher image.')
            else:
                raise APIException('No payment method specified.')
            user.status = 'Pending Approval'
            user.save()
            data = UserSerializer(user, many=False).data
            return Response(data)

    @list_route(methods=['POST'])
    def social_login(self, request):
        data = request.data
        if request.user.is_authenticated:
            return Response(UserSerializer(self.request.user, many=False).data)
        try:
            user = SocialLoginToken.get_user(data)
        except ValueError as e:
            raise APIException(str(e))
        if not user and data.get('full_name') and data.get('email'):
            user = User.objects.create_user(data.get('email'), full_name=data.get('full_name'))
        if user:
            token, created = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(user, many=False).data
            user_data['token'] = token.key
            return Response(user_data)
        return Response({})

    @list_route(methods=['POST'])
    def logout(self, request):
        user = self.request.user
        if user.is_authenticated:
            try:
                reg_id = request.data.get('reg_id')
                if not reg_id:
                    return Response({'detail': 'reg_id is required.'}, status=400)
                device_type = 'ANDROID'
                # if 'HTTP_USER_AGENT' in request.META:
                #     if request.META.get('HTTP_USER_AGENT').startswith('okhttp'):
                #         device_type = 'ANDROID'
                UserDevice.objects.filter(reg_id=reg_id, user=user, device_type=device_type).update(user=None)

                return Response(status=204)
            except UserDevice.DoesNotExist:
                return Response({'status': 'error', 'detail': 'Not found.'}, 404)
        else:
            return Response({'status': 'error', 'detail': 'Not authenticated.'}, 401)


class CustomObtainAuth(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_active:
            send_email_confirmation(request, user)
            return Response({'detail': 'User is inactive!'}, status=403)
        token, created = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user, many=False).data
        user_data['token'] = token.key
        return Response(user_data)
