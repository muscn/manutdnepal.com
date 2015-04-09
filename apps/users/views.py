import datetime

from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout
from django.views.generic import DetailView
from allauth.account.forms import LoginForm, SignupForm
from django.views.generic.list import ListView
from django.db.models import Max
from auditlog.models import LogEntry
from django.contrib import messages
from django.db.models import Q

from .models import Membership, User, StaffOnlyMixin, group_required, CardStatus
from .forms import MembershipForm, UserForm, UserUpdateForm
from apps.payment.forms import BankDepositForm
from apps.payment.models import BankAccount, Payment, EsewaPayment, DirectPayment
from muscn.utils.mixins import UpdateView, CreateView, DeleteView
from apps.payment.forms import BankDepositPaymentForm, DirectPaymentPaymentForm
from apps.users import membership_settings


def login_register(request):
    if request.user.is_authenticated():
        return redirect(reverse('membership_form'))
    login_form = LoginForm()
    signup_form = SignupForm()
    return render(request, 'account/login_register.html', {'login_form': login_form, 'signup_form': signup_form})


def index(request):
    if request.user.is_authenticated():
        return render(request, 'dashboard_index.html')
    return login(request)


def web_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', **kwargs)
    else:
        if request.method == 'POST':
            if 'remember_me' in request.POST:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)
        return login(request, **kwargs)


def logout(request, next_page=None):
    auth_logout(request)
    if next_page:
        return redirect(next_page)
    return redirect('/')


@login_required
def membership_form(request):
    user = request.user
    try:
        item = user.membership
        # return redirect(reverse('membership_payment'))
    except Membership.DoesNotExist:
        item = Membership(user=user)
    # item = Membership(user=user)
    accounts = sorted(user.socialaccount_set.all(), key=lambda x: x.provider, reverse=True)
    for account in accounts:
        if account.provider == 'facebook':
            extra_data = account.extra_data
            try:
                item.gender = extra_data['gender'][:1].upper()
            except KeyError:
                pass
            try:
                item.date_of_birth = datetime.datetime.strptime(extra_data['birthday'], '%m/%d/%Y').strftime('%Y-%m-%d')
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

    if request.POST:
        form = MembershipForm(request.POST, request.FILES, instance=item, user=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('membership_payment'))
    else:
        form = MembershipForm(instance=item, user=request.user)
    return render(request, 'membership_form.html', {
        'form': form,
        'base_template': 'base.html',
    })


@login_required
def membership_payment(request):
    # check if membership form has been received
    try:
        membership = request.user.membership
        if membership.status == 'A':
            return redirect(reverse('view_profile'))
        elif membership.status == 'E':
            return redirect(reverse('renew_membership'))
    except Membership.DoesNotExist:
        return redirect(reverse('membership_form'))
    if request.POST:
        # TODO handle other payment methods
        bank_deposit_form = BankDepositForm(request.POST, request.FILES)
        from apps.users import membership_settings

        payment = Payment(user=request.user, amount=membership_settings.membership_fee)
        payment.save()
        bank_deposit = bank_deposit_form.save(commit=False)
        bank_deposit.payment = payment
        bank_deposit.save()
        membership.payment = payment
        membership.save()
        return redirect(reverse('membership_thankyou'))
    else:
        bank_deposit_form = BankDepositForm()
    bank_accounts = BankAccount.objects.all()
    return render(request, 'membership_payment.html', {
        'membership': membership,
        'bank_deposit_form': bank_deposit_form,
        'bank_accounts': bank_accounts,
        'base_template': 'base.html',
    })


@login_required
def membership_thankyou(request):
    try:
        membership = request.user.membership
    except Membership.DoesNotExist:
        return redirect(reverse('membership_form'))
    if not membership.payment:
        return redirect(reverse('membership_payment'))
    return render(request, 'membership_thankyou.html', {
        'membership': membership,
        'base_template': 'base.html',
    })


class PublicMembershipListView(ListView):
    model = User
    template_name = 'users/members_list.html'

    def get(self, request, *args, **kwargs):
        if 'q' in self.request.GET:
            q = self.request.GET['q']
            self.queryset = User.objects.filter(
                Q(username__icontains=q) |
                Q(full_name__icontains=q) |
                Q(email__icontains=q) |
                Q(devil_no__contains=q) |
                Q(membership__telephone__contains=q) |
                Q(membership__mobile__contains=q)
            )
        return super(PublicMembershipListView, self).get(request, *args, **kwargs)


class MembershipListView(StaffOnlyMixin, ListView):
    model = Membership

    def get(self, request, *args, **kwargs):
        if 'q' in self.request.GET:
            q = self.request.GET['q']
            self.queryset = Membership.objects.filter(
                Q(user__username__icontains=q) |
                Q(user__full_name__icontains=q) |
                Q(user__email__icontains=q) |
                Q(user__devil_no__contains=q) |
                Q(telephone__contains=q) |
                Q(mobile__contains=q)
            )
        return super(MembershipListView, self).get(request, *args, **kwargs)


class MembershipCreateView(StaffOnlyMixin, CreateView):
    model = Membership
    form_class = MembershipForm
    success_url = reverse_lazy('list_memberships')

    def get_form(self, form_class):
        form = super(MembershipCreateView, self).get_form(form_class)
        form.instance.user = User.objects.get(pk=self.kwargs['pk'])
        form.fields['full_name'].initial = form.instance.user.full_name
        return form


class MembershipUpdateView(StaffOnlyMixin, UpdateView):
    model = Membership
    form_class = MembershipForm
    success_url = reverse_lazy('list_memberships')

    def post(self, request, *args, **kwargs):
        if 'action' in request.POST:
            obj = self.get_object()

            if request.POST['action'] == 'Approve':
                if not hasattr(obj, 'payment') or not obj.payment:
                    messages.error(request, 'No payment associated with the membership!')
                elif not obj.payment.verified:
                    messages.error(request, 'Associated payment hasn\'t been verified!')
                else:
                    obj.approved_by = request.user
                    if not obj.user.devil_no:
                        max_devil_no = User.objects.aggregate(Max('devil_no'))['devil_no__max']
                        if max_devil_no is None:
                            max_devil_no = 100
                        obj.user.devil_no = max_devil_no + 1
                        obj.user.save()
                    obj.approved_date = datetime.datetime.now()
                    messages.info(request, 'The membership is approved!')
                    obj.save()
                    if not hasattr(obj, 'card_status'):
                        card_status = CardStatus(membership=obj, status=1)
                        card_status.save()
            elif request.POST['action'] == 'Disprove':
                obj.approved_by = None
                messages.info(request, 'The membership is disproved!')
                obj.save()
            elif request.POST['action'] == 'Download Card':
                return obj.user.get_card_download()
            return redirect(reverse_lazy('update_membership', kwargs={'pk': obj.pk}))
        else:
            return super(MembershipUpdateView, self).post(request, *args, **kwargs)

    def get_form(self, form_class):
        form = super(MembershipUpdateView, self).get_form(form_class)
        form.fields['full_name'].initial = form.instance.user.full_name
        return form


class MembershipDeleteView(StaffOnlyMixin, DeleteView):
    model = Membership
    success_url = reverse_lazy('list_memberships')


class UserListView(StaffOnlyMixin, ListView):
    model = User

    def get(self, request, *args, **kwargs):
        if 'q' in self.request.GET:
            q = self.request.GET['q']
            self.queryset = User.objects.filter(
                Q(username__icontains=q) |
                Q(full_name__icontains=q) |
                Q(email__icontains=q) |
                Q(devil_no__contains=q) |
                Q(membership__telephone__contains=q) |
                Q(membership__mobile__contains=q)
            )
        return super(UserListView, self).get(request, *args, **kwargs)


class UserCreateView(StaffOnlyMixin, CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('list_users')


class UserUpdateView(StaffOnlyMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('list_users')


class UserDeleteView(StaffOnlyMixin, DeleteView):
    model = User
    success_url = reverse_lazy('list_users')


class StaffListView(StaffOnlyMixin, ListView):
    model = User
    template_name = 'users/staff_list.html'

    def get_queryset(self):
        queryset = User.objects.filter(groups__name='Staff')
        return queryset


class StaffDetailView(StaffOnlyMixin, DetailView):
    model = User
    template_name = 'users/staff_detail.html'

    def get_queryset(self):
        queryset = User.objects.filter(groups__name='Staff')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(StaffDetailView, self).get_context_data(**kwargs)
        staff = self.get_object()
        context['memberships_approved'] = staff.memberships_approved.all()
        context['payments_verified'] = staff.verified_payments.all()
        context['audit_log'] = LogEntry.objects.filter(actor=staff)
        return context


@group_required('Staff')
def new_user_membership(request):
    user_form = UserForm(prefix='uf')
    member_form = MembershipForm(prefix='mf')

    payment_initial = {
        'amount': membership_settings.membership_fee,
        'date_time': datetime.datetime.now()
    }
    bank_deposit_form = BankDepositPaymentForm(prefix='bf', initial=payment_initial)
    direct_payment_form = DirectPaymentPaymentForm(prefix='df', initial=payment_initial)
    if request.POST:

        user_form = UserForm(request.POST, request.FILES, prefix='uf')
        member_form = MembershipForm(request.POST, request.FILES, prefix='mf', exclude='full_name')

        # find out the payment form from the hidden field
        if request.POST['payment_method'] == 'bank-deposit':
            bank_deposit_form = BankDepositPaymentForm(request.POST, request.FILES, prefix='bf', exclude='user')
            payment_form = bank_deposit_form
        elif request.POST['payment_method'] == 'direct-payment':
            direct_payment_form = DirectPaymentPaymentForm(request.POST, prefix='df', exclude='user')
            payment_form = direct_payment_form

        if user_form.is_valid() and member_form.is_valid() and payment_form.is_valid():
            user = user_form.save()
            payment_method = payment_form.save(user=user)
            membership = member_form.save(commit=False)
            membership.user = user
            membership.payment = payment_method.payment
            membership.save()
            return redirect(reverse_lazy('list_memberships'))
    context = {
        'user_form': user_form,
        'membership_form': member_form,
        'bank_deposit_form': bank_deposit_form,
        'direct_payment_form': direct_payment_form,
    }
    return render(request, 'users/new_user_membership.html', context)


def esewa_success(request):
    # {u'oid': [u'm_2_2015'], u'amt': [u'150'], u'refId': [u'0000ELD']}
    response = dict(request.GET)
    membership = request.user.membership
    payment = Payment(user=request.user, amount=membership_settings.membership_fee)
    esewa_payment = EsewaPayment(amount=payment.amount, pid=response['oid'][0], ref_id=response['refId'][0])
    if esewa_payment.verify():
        payment.save()
        esewa_payment.payment = payment
        esewa_payment.get_details()
        esewa_payment.save()
        membership.payment = payment
        membership.save()
        messages.success(request, 'Membership fee received via eSewa.')
        return redirect(reverse('membership_thankyou'))
    else:
        messages.error(request, 'Payment via eSewa failed!')
        return redirect('membership_payment')


def esewa_failure(request):
    # {u'q': [u'fu']}
    messages.error(request, 'eSewa transaction failed or cancelled!')
    return redirect('membership_payment')


def download_all_cards(request):
    filtered = [x for x in Membership.objects.all() if x.approved()]


def devil_no_handler(request, devil_no):
    if int(devil_no) < 100:
        raise Http404('Member does not exist!')
    user = get_object_or_404(User, devil_no=devil_no)
    return redirect(reverse_lazy('view_member_profile', kwargs={'slug': user.username}))


class MemberProfileView(DetailView):
    model = Membership
    slug_field = 'user__username'


class DirectPaymentForMembershipCreateView(StaffOnlyMixin, CreateView):
    model = DirectPayment
    form_class = DirectPaymentPaymentForm
    # success_url = reverse_lazy('list_memberships')

    def get_success_url(self):
        return reverse_lazy('update_direct_payment', kwargs={'pk': self.object.id})

    def get_initial(self):
        membership = get_object_or_404(Membership, id=self.kwargs['pk'])
        return {'amount': membership_settings.membership_fee, 'received_by': self.request.user, 'user': membership.user,
                'date_time': datetime.datetime.now(), 'remarks': 'For Membership'}

    def form_valid(self, form):
        membership = get_object_or_404(Membership, id=self.kwargs['pk'])
        ret = super(DirectPaymentForMembershipCreateView, self).form_valid(form)
        membership.payment = form.instance.payment
        membership.save()
        return ret