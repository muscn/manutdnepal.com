from datetime import date

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, UserChangeForm as DjangoUserChangeForm, \
    UserCreationForm as DjangoUserCreationForm
from django import forms
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from apps.users.models import User, GroupProxy, Membership, CardStatus, Renewal, MembershipSetting, Newsletter
from solo.admin import SingletonModelAdmin


def url_to_edit_object(obj):
    if not obj:
        return 'None'
    url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=(obj.pk,))
    return u'<a href="%s">%s</a>' % (url, obj.__str__())


class UserCreationForm(DjangoUserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta(DjangoUserCreationForm.Meta):
        model = User
        # exclude = ('first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            self._meta.model._default_manager.get(username=username)
        except self._meta.model.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(DjangoUserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    # password = ReadOnlyPasswordHashField(label= ("Password"),
    # help_text= ("Raw passwords are not stored, so there is no way to see "
    # "this user's password, but you can change the password "
    # "using <a href=\"password/\">this form</a>."))

    class Meta(DjangoUserChangeForm.Meta):
        model = User

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    ordering = ('username',)
    filter_horizontal = ()
    list_display = ('id', 'full_name', 'email', 'is_staff', 'devil_no', 'status')
    list_filter = ('is_staff', 'is_superuser', 'status', 'channel', 'complimentary')
    fieldsets = ((None,
                  {'fields': ('full_name',
                              'devil_no',
                              'status',
                              'mobile',
                              'email',
                              'password',
                              'is_active',
                              'is_staff',
                              'is_superuser',
                              'last_login',
                              'channel',
                              'groups')}),
                 )
    add_fieldsets = ((None,
                      {'classes': ('wide',
                                   ),
                       'fields': ('username',
                                  'email',
                                  'password1',
                                  'password2',
                                  'is_active',
                                  'is_staff',
                                  'is_superuser')}),
                     )
    search_fields = ('id', 'full_name', 'email', 'devil_no')
    readonly_fields = ('is_staff', 'is_superuser')


class DecadeBornListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('decade born')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'decade'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('80s', _('in the eighties')),
            ('90s', _('in the nineties')),
            ('2000s', _('in 2000s')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == '80s':
            return queryset.filter(date_of_birth__gte=date(1980, 1, 1),
                                   date_of_birth__lte=date(1989, 12, 31))
        if self.value() == '90s':
            return queryset.filter(date_of_birth__gte=date(1990, 1, 1),
                                   date_of_birth__lte=date(1999, 12, 31))
        if self.value() == '2000s':
            return queryset.filter(date_of_birth__gte=date(1999, 12, 31))


def make_awaiting(modeladmin, request, queryset):
    queryset.update(status='Awaiting Print')
    [obj.notify() for obj in queryset]


make_awaiting.short_description = "Set as 'Awaiting Print'"


def make_printed(modeladmin, request, queryset):
    queryset.update(status='Printed')
    queryset.update(remarks='')
    [obj.notify() for obj in queryset]


make_printed.short_description = "Set as 'Printed'"


def make_delivered(modeladmin, request, queryset):
    queryset.update(status='Delivered')
    [obj.notify() for obj in queryset]


make_delivered.short_description = "Set as 'Delivered'"


class CardStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_devil_no', 'status', 'pickup_location')
    search_fields = ('user__full_name', 'user__devil_no', 'user__mobile', 'user__email')
    list_filter = ('status', 'season', 'pickup_location')
    actions = [make_awaiting, make_printed, make_delivered]

    def save_model(self, request, obj, form, change):
        if 'status' in form.initial and not form.initial['status'] == obj.status:
            obj.notify()
        obj.save()

    def get_devil_no(self, obj):
        return obj.user.devil_no

    get_devil_no.short_description = 'Devil #'
    get_devil_no.admin_order_field = 'membership__user__devil_no'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'pickup_location')


admin.site.register(User, CustomUserAdmin)


# Removing default apps
# admin.site.unregister(Site)

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('key', 'subject')
    search_fields = ('key', 'subject', 'body')
    readonly_fields = ('last_sent',)


admin.site.register(Newsletter, NewsletterAdmin)

from django.contrib.auth.models import Group

admin.site.unregister(Group)
admin.site.register(GroupProxy)
admin.site.register(CardStatus, CardStatusAdmin)
admin.site.register(MembershipSetting, SingletonModelAdmin)
