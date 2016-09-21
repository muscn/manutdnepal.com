import uuid

from django.contrib import admin

from .models import DistributedKey


class DistributedKeyAdmin(admin.ModelAdmin):
    readonly_fields = ('key',)
    list_display = ('client_name', 'key',)
    actions = ['regenerate_key', ]

    def regenerate_key(self, request, queryset):
        for obj in queryset:
            obj.key = uuid.uuid4().hex
            obj.save()

    regenerate_key.short_description = "Regenerate Key for selected clients."


admin.site.register(DistributedKey, DistributedKeyAdmin)
