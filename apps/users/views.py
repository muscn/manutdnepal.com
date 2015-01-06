from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout
from .models import Membership, User
from .forms import MembershipForm, UserForm, UserUpdateForm
from apps.payment.forms import BankDepositForm
from apps.payment.models import BankAccount, Payment
from allauth.account.forms import LoginForm, SignupForm
import datetime
from django.views.generic.list import ListView
from muscn.utils.mixins import UpdateView, CreateView, DeleteView
from apps.payment.forms import BankDepositPaymentForm, DirectPaymentPaymentForm


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
        membership = user.membership
        return redirect(reverse('membership_payment'))
    except Membership.DoesNotExist:
        pass
    item = Membership(user=user)
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


class MembershipListView(ListView):
    model = Membership


class MembershipCreateView(CreateView):
    model = Membership
    form_class = MembershipForm
    success_url = reverse_lazy('list_memberships')

    def get_form(self, form_class):
        form = super(MembershipCreateView, self).get_form(form_class)
        form.instance.user = User.objects.get(pk=self.kwargs['pk'])
        form.fields['full_name'].initial = form.instance.user.full_name
        return form


class MembershipUpdateView(UpdateView):
    model = Membership
    form_class = MembershipForm
    success_url = reverse_lazy('list_memberships')

    def get_form(self, form_class):
        form = super(MembershipUpdateView, self).get_form(form_class)
        form.fields['full_name'].initial = form.instance.user.full_name
        return form


class MembershipDeleteView(DeleteView):
    model = Membership
    success_url = reverse_lazy('list_memberships')


class UserListView(ListView):
    model = User


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('list_users')


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('list_users')


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('list_users')


def new_user_membership(request):
    user_form = UserForm(prefix='uf')
    member_form = MembershipForm(prefix='mf')
    bank_deposit_form = BankDepositPaymentForm()
    direct_payment_form = DirectPaymentPaymentForm(prefix='df')
    if request.POST:
        pass
    context = {
        'user_form': user_form,
        'membership_form': member_form,
        'bank_deposit_form': bank_deposit_form,
        'direct_payment_form': direct_payment_form,
    }
    return render(request, 'users/new_user_membership.html', context)
