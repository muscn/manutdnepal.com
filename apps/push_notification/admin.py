import datetime

from django.conf import settings

from django.contrib import admin
from fcm.utils import get_device_model
import pytz

from .models import BulkMessage

Device = get_device_model()


def send(modeladmin, request, queryset):
    devices = Device.objects.all()
    for bulk_message in queryset:
        device_response = devices.send_message({'message': bulk_message.message})
        bulk_message.response_message = device_response
        bulk_message.last_sent_at = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        bulk_message.save()


class BulkMessageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at', 'updated_at', 'last_sent_at')
    list_filter = ('created_at', 'updated_at', 'last_sent_at')
    readonly_fields = ['created_at', 'updated_at', 'last_sent_at']
    actions = [send, ]


admin.site.register(BulkMessage, BulkMessageAdmin)
