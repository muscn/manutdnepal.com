from django.contrib import messages
from django.contrib.admin.filters import RelatedFieldListFilter


def send_action(modeladmin, request, queryset):
    for obj in queryset:
        obj.send()
    messages.success(request, 'Sent %d message(s)' % queryset.count())


send_action.short_description = 'Send'


class StaffFilter(RelatedFieldListFilter):
    def __init__(self, field, request, *args, **kwargs):
        field.rel.limit_choices_to = {'is_staff': True}
        super(StaffFilter, self).__init__(field, request, *args, **kwargs)
