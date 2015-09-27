from django.contrib import admin
from .models import Timeline, TimelineEvent, Location


class EventInline(admin.TabularInline):
    model = Timeline.events.through


class TimelineEventAdmin(admin.ModelAdmin):
    inlines = [EventInline]


class TimelineAdmin(admin.ModelAdmin):
    inlines = [EventInline]
    exclude = ('events', )


admin.site.register(Timeline, TimelineAdmin)
admin.site.register(TimelineEvent, TimelineEventAdmin)
admin.site.register(Location)
