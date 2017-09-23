from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.list import ListView

from muscn.utils.mixins import UpdateView, CreateView, DeleteView
from .models import Payment, BankAccount, BankDeposit, DirectPayment, EsewaPayment
from .forms import PaymentForm, BankAccountForm, BankDepositPaymentForm, DirectPaymentForm
from apps.users.models import StaffOnlyMixin


class PaymentListView(StaffOnlyMixin, ListView):
    model = Payment


class PaymentUpdateView(StaffOnlyMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    success_url = reverse_lazy('list_payments')

    def post(self, request, *args, **kwargs):
        if 'action' in request.POST:
            obj = self.get_object()
            if request.POST['action'] == 'Approve':
                obj.verified_by = request.user
                messages.info(request, 'The payment is approved!')
            elif request.POST['action'] == 'Disprove':
                obj.verified_by = None
                messages.info(request, 'The payment is disproved!')
            obj.save()
            return redirect(reverse_lazy('update_payment', kwargs={'pk': obj.pk}))
        else:
            return super(PaymentUpdateView, self).post(request, *args, **kwargs)


class PaymentCreateView(StaffOnlyMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    success_url = reverse_lazy('list_payments')


class PaymentDeleteView(StaffOnlyMixin, DeleteView):
    model = Payment
    success_url = reverse_lazy('list_payments')


class BankAccountListView(StaffOnlyMixin, ListView):
    model = BankAccount


class BankAccountUpdateView(StaffOnlyMixin, UpdateView):
    model = BankAccount
    form_class = BankAccountForm
    success_url = reverse_lazy('list_bank_accounts')


class BankAccountCreateView(StaffOnlyMixin, CreateView):
    model = BankAccount
    form_class = BankAccountForm
    success_url = reverse_lazy('list_bank_accounts')


class BankAccountDeleteView(StaffOnlyMixin, DeleteView):
    model = BankAccount
    success_url = reverse_lazy('list_bank_accounts')


class BankDepositListView(StaffOnlyMixin, ListView):
    model = BankDeposit


class BankDepositCreateView(StaffOnlyMixin, CreateView):
    model = BankDeposit
    form_class = BankDepositPaymentForm
    success_url = reverse_lazy('list_bank_deposits')


class BankDepositUpdateView(StaffOnlyMixin, UpdateView):
    model = BankDeposit
    form_class = BankDepositPaymentForm
    success_url = reverse_lazy('list_bank_deposits')


class BankDepositDeleteView(StaffOnlyMixin, DeleteView):
    model = BankDeposit
    success_url = reverse_lazy('list_bank_deposits')


class DirectPaymentListView(StaffOnlyMixin, ListView):
    model = DirectPayment


class DirectPaymentCreateView(StaffOnlyMixin, CreateView):
    model = DirectPayment
    form_class = DirectPaymentForm
    success_url = reverse_lazy('list_direct_payments')


class DirectPaymentUpdateView(StaffOnlyMixin, UpdateView):
    model = DirectPayment
    form_class = DirectPaymentForm
    success_url = reverse_lazy('list_direct_payments')


class DirectPaymentDeleteView(StaffOnlyMixin, DeleteView):
    model = DirectPayment
    success_url = reverse_lazy('list_direct_payments')


class EsewaPaymentListView(StaffOnlyMixin, ListView):
    model = EsewaPayment

def move_bank_to_direct_payment(request, pk=None):
    bank_deposit = BankDeposit.objects.get(pk=pk)
    direct = DirectPayment()
    direct.payment = bank_deposit.payment
    direct.receipt_image = bank_deposit.voucher_image
    direct.receipt_no = 0
    direct.save()
    #proxy payment, deleted while bank_deposit is deleted
    payment = Payment(amount=100, user=request.user)
    payment.save()
    bank_deposit.payment = payment
    bank_deposit.delete()
    return redirect(reverse('update_direct_payment', kwargs={'pk': direct.id}))