# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import ContactSetting, Message

admin.site.register(ContactSetting, SingletonModelAdmin)


class MesageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'message')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')


admin.site.register(Message, MesageAdmin)
