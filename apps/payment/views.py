from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from muscn.utils.mixins import UpdateView
from .models import Payment
from .forms import PaymentForm


class PaymentListView(ListView):
    model = Payment


class PaymentUpdateView(UpdateView):
    model = Payment
    form_class = PaymentForm
    success_url = reverse_lazy('list_payments')

    def get(self, request, *args, **kwargs):
        if 'disprove' in request.GET:
            obj = self.get_object()
            obj.verified_by = None
            obj.save()
        if 'approve' in request.GET:
            obj = self.get_object()
            obj.verified_by = request.user
            obj.save()
        return super(PaymentUpdateView, self).get(request, *args, **kwargs)