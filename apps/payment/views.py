from django.core.urlresolvers import reverse_lazy
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


# def list_payments(request):
# all_payments = Payment.objects.all()
# context = {
#         'object_list': all_payments
#     }
#     return render(request, 'payment_list.html', context)


