from django.contrib import admin
from .models import Timeline, TimelineEvent, Location


class EventInline(admin.TabularInline):
    model = TimelineEvent
    fk_name = 'timeline'


class TimelineAdmin(admin.ModelAdmin):
    inlines = [EventInline]


admin.site.register(Timeline, TimelineAdmin)
admin.site.register(TimelineEvent)
admin.site.register(Location)
