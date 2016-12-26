from django.contrib import admin
from .models import Payment, DirectPayment, BankAccount, BankDeposit, EsewaPayment, ReceiptData


class ReceiptDataAdmin(admin.ModelAdmin):
    list_display = ('name', 'from_no', 'to_no')
    search_fields = ('name', 'from_no', 'to_no')


admin.site.register(Payment)
admin.site.register(DirectPayment)
admin.site.register(BankDeposit)
admin.site.register(BankAccount)
admin.site.register(EsewaPayment)
admin.site.register(ReceiptData, ReceiptDataAdmin)
