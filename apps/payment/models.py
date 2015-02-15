from django.core.urlresolvers import reverse_lazy
from django.db import models
from django.conf import settings
import datetime
from auditlog.registry import auditlog

User = settings.AUTH_USER_MODEL


class Payment(models.Model):
    user = models.ForeignKey(User, blank=False, verbose_name='By')
    date_time = models.DateTimeField(default=datetime.datetime.now, verbose_name='Date/Time')
    amount = models.FloatField()
    verified_by = models.ForeignKey(User, blank=True, null=True, related_name='verified_payments')
    remarks = models.TextField(blank=True, null=True)

    def delete(self, delete_method=True, *args, **kwargs):
        if delete_method and self.method:
            self.method.delete(delete_payment=False)
        return super(Payment, self).delete(*args, **kwargs)

    @property
    def method(self):
        # methods are related name on one-to-one payment fields on payment methods
        methods = ('bank_deposit', 'direct_payment')
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

    def __unicode__(self):
        return unicode(self.user) + ' - ' + unicode(self.date_time) + ' - ' + unicode(self.amount)

    @property
    def list_payment_for(self):
        return self.payment_for.all()

    @property
    def verified(self):
        return True if self.verified_by and self.method else False


class BankAccount(models.Model):
    bank_name = models.CharField(max_length=255)
    ac_no = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.bank_name + ' (A/C No.: ' + str(self.ac_no) + ' )'


class BankDeposit(models.Model):
    bank = models.ForeignKey(BankAccount)
    voucher_image = models.ImageField(upload_to='voucher_images/')
    payment = models.OneToOneField(Payment, related_name='bank_deposit')

    def delete(self, delete_payment=True, *args, **kwargs):
        if delete_payment and self.payment:
            self.payment.delete(delete_method=False)
        return super(BankDeposit, self).delete(*args, **kwargs)

    def verified(self):
        return True if self.payment.verified_by else False

    def get_absolute_url(self):
        return reverse_lazy('update_bank_deposit', kwargs={'pk': self.pk})

    def __unicode__(self):
        return unicode(self.payment.user) + ' - ' + unicode(self.payment.date_time) + ' - ' + unicode(
            self.payment.amount) + '-' + unicode(self.bank)


class DirectPayment(models.Model):
    received_by = models.ForeignKey(User)
    payment = models.OneToOneField(Payment, related_name='direct_payment')

    def verified(self):
        return True if self.payment.verified_by else False

    def delete(self, delete_payment=True, *args, **kwargs):
        if delete_payment and self.payment:
            self.payment.delete(delete_method=False)
        return super(DirectPayment, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('update_direct_payment', kwargs={'pk': self.pk})

    def __unicode__(self):
        return unicode(self.payment.user) + ' - ' + unicode(self.payment.date_time) + ' - ' + unicode(
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


auditlog.register(Payment)
auditlog.register(BankAccount)