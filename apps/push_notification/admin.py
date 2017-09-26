from django.contrib import admin

from .models import PushMessage, UserDevice
from muscn.utils.admin import StaffFilter, send_action

from fcm.models import Device


class UserDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'dev_id', 'name', 'device_type', 'is_active', 'created_at', 'updated_at')
    list_filter = ('device_type', 'is_active')
    readonly_fields = ('created_at', 'updated_at')


class PushMessageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'created_at', 'updated_at', 'last_sent_at')
    list_filter = (('author', StaffFilter), 'created_at', 'updated_at', 'last_sent_at')
    readonly_fields = ['author', 'created_at', 'updated_at', 'last_sent_at']
    actions = [send_action, ]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


admin.site.register(PushMessage, PushMessageAdmin)
admin.site.register(UserDevice, UserDeviceAdmin)
admin.site.unregister(Device)
