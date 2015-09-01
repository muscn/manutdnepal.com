from django.contrib import admin
from .models import Payment, DirectPayment, BankAccount, BankDeposit, EsewaPayment

admin.site.register(Payment)
admin.site.register(DirectPayment)
admin.site.register(BankDeposit)
admin.site.register(BankAccount)
admin.site.register(EsewaPayment)