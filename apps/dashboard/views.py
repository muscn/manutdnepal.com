from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from apps.payment.models import Payment
from apps.users.models import group_required, User
from django.views.generic.list import ListView
from auditlog.models import LogEntry


@group_required('Staff')
def index(request):
    return render(request, 'dashboard_index.html')


class AuditLogListView(ListView):
    model = LogEntry


@group_required('Staff')
def approve_payment_membership(request):
    if not request.method == 'POST':
        raise Http404
    data = request.POST
    user = User.objects.get(pk=data.get('user_id'), status='Pending Approval')
    payment = Payment.objects.get(pk=data.get('payment_id'), user=user)
    payment.verified_by = request.user
    payment.save()
    user.approve()
    messages.success(request, 'Payment and membership approved!')
    return redirect(reverse_lazy('update_user', kwargs={'pk': user.id}))


@group_required('Staff')
def approve_membership(request):
    if not request.method == 'POST':
        raise Http404
    data = request.POST
    user = User.objects.get(pk=data.get('user_id'), status='Pending Approval')
    payment = Payment.objects.get(pk=data.get('payment_id'), user=user)
    if payment.verified:
        user.approve()
        messages.success(request, 'Membership approved!')
    return redirect(reverse_lazy('update_user', kwargs={'pk': user.id}))


def approve_complimentary_membership(request):
    if not request.method == 'POST':
        raise Http404
    data = request.POST
    user = User.objects.get(pk=data.get('user_id'), complimentary=True)
    user.approve()
    messages.success(request, 'Complimentary Membership approved!')
    user.complimentary = False
    user.save()
    return redirect(reverse_lazy('update_user', kwargs={'pk': user.id}))
