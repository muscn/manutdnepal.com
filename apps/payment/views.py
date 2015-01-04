from django.views.generic.list import ListView
from .models import Payment


class PaymentListView(ListView):
    model = Payment


# def list_payments(request):
# all_payments = Payment.objects.all()
#     context = {
#         'object_list': all_payments
#     }
#     return render(request, 'payment_list.html', context)


