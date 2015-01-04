from django.views.generic.list import ListView
from muscn.utils.mixins import UpdateView
from .models import Payment
from .forms import PaymentForm


class PaymentListView(ListView):
    model = Payment


class PaymentUpdateView(UpdateView):
    model = Payment
    form_class = PaymentForm


# def list_payments(request):
# all_payments = Payment.objects.all()
# context = {
#         'object_list': all_payments
#     }
#     return render(request, 'payment_list.html', context)


