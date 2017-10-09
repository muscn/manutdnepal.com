from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from .models import Partner


class PartnerAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'short_address', 'order')


admin.site.register(Partner, PartnerAdmin)
