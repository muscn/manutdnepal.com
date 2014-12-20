from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout
from users.models import Membership
from users.forms import MembershipForm
from payment.forms import BankDepositForm
from payment.models import BankAccount, BankDeposit, Payment
from allauth.account.forms import LoginForm, SignupForm
import datetime


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
    try:
        membership = request.user.membership
        return redirect(reverse('membership_payment'))
    except Membership.DoesNotExist:
        pass
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
        form = MembershipForm(request.POST, request.FILES, instance=item, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('membership_payment'))
    else:
        form = MembershipForm(instance=item, user=request.user)
    return render(request, 'membership_form.html', {
        'form': form,
        'base_template': 'base.html',
    })


def membership_payment(request):
    # check if membership form has been received
    try:
        membership = request.user.membership
    except Membership.DoesNotExist:
        return redirect(reverse('membership_form'))
    if request.POST:
        # TODO handle other payment methods
        bank_deposit_form = BankDepositForm(request.POST, request.FILES)
        # bank_deposit = Payment.create(request.user, 500, bank_deposit_form.save(commit=False))
        # bank_deposit.save()
        # membership.payment =
        # TODO Membership fee from settings
        payment = Payment(user=request.user, amount=500)
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