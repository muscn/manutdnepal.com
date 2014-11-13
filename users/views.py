from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout
from users.models import Membership
from users.forms import MembershipForm


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
    item, new = Membership.objects.get_or_create(user=request.user)
    if request.POST:
        form = MembershipForm(data=request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            return redirect('/')
    else:
        form = MembershipForm(instance=item)
    return render(request, 'membership_form.html', {
        'form': form,
        'base_template': 'base.html',
    })