from django.contrib import admin
from page.models import Page, Category
from page.forms import PageForm


class PageAdmin(admin.ModelAdmin):
    form = PageForm

    def get_form(self, request, *args, **kwargs):
        form = super(PageAdmin, self).get_form(request, *args, **kwargs)
        form.base_fields['author'].initial = request.user
        return form


admin.site.register(Page, PageAdmin)
admin.site.register(Category)
