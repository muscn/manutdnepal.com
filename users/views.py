from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout
from users.models import Membership
from users.forms import MembershipForm
import datetime


def index(request):
    if request.user.is_authenticated():
        return render(request, 'dashboard_index.html')
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
    item = Membership(user=request.user)
    item.gender = 'F'
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
                # import ipdb
                #
                # ipdb.set_trace()

    if request.POST:
        form = MembershipForm(data=request.POST, instance=item, user=request.user)
        if form.is_valid():
            item = form.save()
            return redirect('/')
    else:
        form = MembershipForm(instance=item, user=request.user)
    return render(request, 'membership_form.html', {
        'form': form,
        'base_template': 'base.html',
    })