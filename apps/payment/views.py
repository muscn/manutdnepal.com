from django.shortcuts import render


def list_payments(request):
    return render(request, 'list_payments.html')
