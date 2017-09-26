from __future__ import unicode_literals
import datetime
from django.conf import settings

from django.db import models
from fcm.models import AbstractDevice
import pytz

from ..users.models import User


class UserDevice(AbstractDevice):
    TYPES = (
        ('ANDROID', 'ANDROID'),
        # ('IOS', 'IOS'),
    )
    user = models.ForeignKey(User, related_name='devices', null=True, blank=True)
    device_type = models.CharField(choices=TYPES, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def send_all(cls, msg):
        cls.objects.filter(is_active=True).send_message(msg)

    def __str__(self):
        return 'FCM Device for %s' % self.user


class PushMessage(models.Model):
    title = models.CharField(max_length=255, default='Man Utd.')
    message = models.TextField()
    url = models.URLField(blank=True, null=True)
    remarks = models.TextField(null=True, blank=True, help_text='Admin notes.')
    response_message = models.TextField(null=True, blank=True, help_text='FCM response.')
    author = models.ForeignKey(User, related_name='push_messages', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    last_sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        # truncate to 75 chars
        char_len = 75
        return (self.message[:char_len] + '..') if len(self.message) > char_len else self.message

    def send(self):
        response = UserDevice.objects.filter(is_active=True).send_message(
            {'type': 'message', 'message': self.message, 'title': self.title, 'url': self.url})
        self.response_message = response
        self.last_sent_at = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        self.save()
