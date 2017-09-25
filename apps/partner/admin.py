from django.contrib import admin
from .models import Partner


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_address', 'order')


admin.site.register(Partner, PartnerAdmin)
