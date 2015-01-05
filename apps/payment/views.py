from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.list import ListView
from muscn.utils.mixins import UpdateView, CreateView, DeleteView
from .models import Payment, BankAccount, BankDeposit, DirectPayment
from .forms import PaymentForm, BankAccountForm, BankDepositPaymentForm


class PaymentListView(ListView):
    model = Payment


class PaymentUpdateView(UpdateView):
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


class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    success_url = reverse_lazy('list_payments')


class PaymentDeleteView(DeleteView):
    model = Payment
    success_url = reverse_lazy('list_payments')


class BankAccountListView(ListView):
    model = BankAccount


class BankAccountUpdateView(UpdateView):
    model = BankAccount
    form_class = BankAccountForm
    success_url = reverse_lazy('list_bank_accounts')


class BankAccountCreateView(CreateView):
    model = BankAccount
    form_class = BankAccountForm
    success_url = reverse_lazy('list_bank_accounts')


class BankAccountDeleteView(DeleteView):
    model = BankAccount
    success_url = reverse_lazy('list_bank_accounts')


class BankDepositListView(ListView):
    model = BankDeposit


class BankDepositCreateView(CreateView):
    model = BankDeposit
    form_class = BankDepositPaymentForm
    success_url = reverse_lazy('list_bank_deposits')


class BankDepositUpdateView(UpdateView):
    model = BankDeposit
    form_class = BankDepositPaymentForm
    success_url = reverse_lazy('list_bank_deposits')


class BankDepositDeleteView(DeleteView):
    model = BankDeposit
    success_url = reverse_lazy('list_bank_deposits')


class DirectPaymentListView(ListView):
    model = DirectPayment