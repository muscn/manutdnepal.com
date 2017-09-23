import datetime

from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.conf import settings
from auditlog.registry import auditlog
from django.utils import timezone

from apps.payment.esewa import EsewaTransaction
from muscn.utils.football import get_current_season_start

User = settings.AUTH_USER_MODEL


class Payment(models.Model):
    user = models.ForeignKey(User, blank=False, verbose_name='By')
    date_time = models.DateTimeField(default=timezone.now, verbose_name='Date/Time')
    amount = models.FloatField()
    verified_by = models.ForeignKey(User, blank=True, null=True, related_name='verified_payments')
    remarks = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.verified:
            for renewal in self.renewals.all():
                renewal.membership.expiry_date = get_current_season_start() + datetime.timedelta(days=365)
                # Set card status to awaiting print
                renewal.membership.set_card_status(1)
                # If the membership model doesn't have payment, it isn't reckoned to be approved
                # Set the renewal payment as membership payment
                if not renewal.membership.payment_id:
                    renewal.membership.payment = self
                # Same with approved_by
                if not renewal.membership.approved_by_id:
                    renewal.membership.approved_by = self.verified_by
                # Also replace the membership payment if it wasn't a verified payment
                if renewal.membership.payment_id and not renewal.membership.payment.verified:
                    renewal.membership.payment = self
                renewal.membership.save()
        super(Payment, self).save(*args, **kwargs)

    def delete(self, delete_method=True, *args, **kwargs):
        if delete_method and self.method:
            self.method.delete(delete_payment=False)
        return super(Payment, self).delete(*args, **kwargs)

    @property
    def method(self):
        # methods are related name on one-to-one payment fields on payment methods
        methods = ('bank_deposit', 'direct_payment', 'esewa_payment')
        for method in methods:
            if hasattr(self, method):
                return getattr(self, method)

    @property
    def method_type(self):
        if self.method:
            return self.method.__class__._meta.verbose_name.title()

    @staticmethod
    def create(user, amount, method):
        payment = Payment(user=user, amount=amount)
        payment.save()
        method.payment = payment
        return method

    def get_absolute_url(self):
        return reverse_lazy('update_payment', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.user) + ' - ' + str(self.date_time) + ' - ' + str(self.amount)

    @property
    def list_payment_for(self):
        return self.payment_for.all()

    @property
    def verified(self):
        return True if self.verified_by and self.method else False

    class Meta:
        ordering = ('-date_time',)


class BankAccount(models.Model):
    bank_name = models.CharField(max_length=255)
    ac_no = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.bank_name + ' (A/C No.: ' + str(self.ac_no) + ' )'


class BankDeposit(models.Model):
    bank = models.ForeignKey(BankAccount)
    voucher_image = models.FileField(upload_to='voucher_images/')
    payment = models.OneToOneField(Payment, related_name='bank_deposit')

    def delete(self, delete_payment=True, *args, **kwargs):
        if delete_payment and self.payment:
            self.payment.delete(delete_method=False)
        return super(BankDeposit, self).delete(*args, **kwargs)

    def verified(self):
        return True if self.payment.verified_by else False

    def get_absolute_url(self):
        return reverse_lazy('update_bank_deposit', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.payment.user) + ' - ' + str(self.payment.date_time) + ' - ' + str(
            self.payment.amount) + '-' + str(self.bank)


class DirectPayment(models.Model):
    received_by = models.ForeignKey(User, null=True, blank=True)
    payment = models.OneToOneField(Payment, related_name='direct_payment')
    receipt_no = models.PositiveIntegerField(null=True, unique=True,
                                             verbose_name='Receipt No. (If you paid directly to a representative)')
    receipt_image = models.ImageField(upload_to='receipt_images/', null=True, blank=True)

    def verified(self):
        return True if self.payment.verified_by else False

    def delete(self, delete_payment=True, *args, **kwargs):
        if delete_payment and self.payment:
            self.payment.delete(delete_method=False)
        return super(DirectPayment, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('update_direct_payment', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.payment.user) + ' - ' + str(self.payment.date_time) + ' - ' + str(
            self.payment.amount)

        #
        # class Service(models.Model):
        # name = models.CharField(max_length=255)
        #
        #
        # class Transaction(models.Model):
        # service = models.ForeignKey(Service)
        # transaction_id = models.TextField(max_length=64)
        # payment = models.ForeignKey(Payment)
        # extra_data = models.JSONField()


class EsewaPayment(EsewaTransaction):
    payment = models.OneToOneField(Payment, related_name='esewa_payment')

    # amount = None

    # class Amount(object):
    #     def __get__(self, instance, owner):
    #         return self.payment.amount
    #
    #     def __set__(self, obj, val):
    #         obj.payment.amount = val

    # amount = Amount()

    def __str__(self):
        return str(self.payment.user) + ' - ' + str(self.payment.amount)

    def get_absolute_url(self):
        return reverse_lazy('update_payment', kwargs={'pk': self.payment.pk})

    def delete(self, delete_payment=True, *args, **kwargs):
        if delete_payment and self.payment:
            self.payment.delete(delete_method=False)
        return super(EsewaPayment, self).delete(*args, **kwargs)


class ReceiptData(models.Model):
    name = models.CharField(max_length=255)
    from_no = models.IntegerField()
    to_no = models.IntegerField()
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s [%d-%d]' % (self.name, self.from_no, self.to_no)

    class Meta:
        verbose_name_plural = 'Receipt Data'


auditlog.register(DirectPayment)
auditlog.register(EsewaPayment)
auditlog.register(BankDeposit)
auditlog.register(BankAccount)
