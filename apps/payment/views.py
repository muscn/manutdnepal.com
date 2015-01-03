from django.shortcuts import render
from .models import Payment


def list_payments(request):
    all_payments = Payment.objects.all()
    context = {
        'all_payments': all_payments
    }
    return render(request, 'list_payments.html', context)
