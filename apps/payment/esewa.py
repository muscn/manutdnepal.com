import urllib
from urllib.parse import urlencode

from django.conf import settings
from django.db import models
import requests
from django.utils import timezone
from jsonfield import JSONField


class EsewaTransaction(models.Model):
    amount = models.FloatField()
    pid = models.CharField(max_length=255)
    ref_id = models.CharField(max_length=25)
    tax_amount = models.FloatField(default=0)
    service_charge = models.FloatField(default=0)
    delivery_charge = models.FloatField(default=0)
    datetime = models.DateTimeField(default=timezone.now)

    details = JSONField()

    def __init__(self, *args, **kwargs):
        self.debug = getattr(settings, 'ESEWA_DEBUG', False)
        self.scd = getattr(settings, 'ESEWA_SCD')
        if self.debug:
            self.url = 'https://dev.esewa.com.np/epay/main'
            self.verification_url = 'https://dev.esewa.com.np/epay/transrec'
            self.transaction_url = 'https://dev.esewa.com.np/epay/transdetails'
        else:
            self.url = 'https://esewa.com.np/epay/main'
            self.verification_url = 'https://esewa.com.np/epay/transrec'
            self.transaction_url = 'https://esewa.com.np/epay/transdetails'
        super(EsewaTransaction, self).__init__(*args, **kwargs)

    def clear_details(self):
        self.details = {}

    def get_details(self):
        if self.details:
            return self.details
        kwargs = {'amt': self.amount, 'pid': self.pid, 'scd': self.scd}
        url = self.transaction_url + '?' + urlencode(kwargs)
        self.details = requests.get(url).json()
        return self.details

    def refresh_details(self):
        self.clear_details()
        return self.get_details()

    def verify(self):
        kwargs = {'amt': self.amount, 'pid': self.pid, 'scd': self.scd, 'rid': self.ref_id}
        url = self.verification_url + '?' + urlencode(kwargs)
        response = requests.get(url)
        if 'Success' in str(response.content) or 'success' in str(response.content):
            return True
        return False

    class Meta:
        abstract = True
