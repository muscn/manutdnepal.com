from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Payment(models.Model):
    user = models.ForeignKey(User)
    date_time = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    verified_by = models.ForeignKey(User, blank=True, null=True, related_name='verified_payments')
    remarks = models.TextField(blank=True, null=True)

    @staticmethod
    def create(user, amount, method):
        payment = Payment(user=user, amount=amount)
        payment.save()
        method.payment = payment
        return method

    def __unicode__(self):
        return unicode(self.user) + ' - ' + unicode(self.date_time) + ' - ' + unicode(self.amount)

    @property
    def verified(self):
        return True if self.verified_by else False


class BankAccount(models.Model):
    bank_name = models.CharField(max_length=255)
    ac_no = models.CharField(max_length=50)
    branch_name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.bank_name + ' Account (' + str(self.ac_no) + ' )'


class BankDeposit(models.Model):
    bank = models.ForeignKey(BankAccount)
    voucher_image = models.ImageField(upload_to='voucher_images/')
    payment = models.ForeignKey(Payment)

    def __unicode__(self):
        return unicode(self.payment.user) + ' - ' + unicode(self.payment.date_time) + ' - ' + unicode(
            self.payment.amount) + '-' + unicode(self.bank)


class DirectPayment(models.Model):
    received_by = models.ForeignKey(User)
    payment = models.ForeignKey(Payment)

    def __unicode__(self):
        return unicode(self.payment.user) + ' - ' + unicode(self.payment.date_time) + ' - ' + unicode(
            self.payment.amount)

#
# class Service(models.Model):
#     name = models.CharField(max_length=255)
#
#
# class Transaction(models.Model):
#     service = models.ForeignKey(Service)
#     transaction_id = models.TextField(max_length=64)
#     payment = models.ForeignKey(Payment)
#     extra_data = models.JSONField()