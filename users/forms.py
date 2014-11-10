from django import forms
from users.models import User
from django.contrib.auth.models import Group


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'is_active',
                  'is_staff', 'is_admin', 'last_login', 'groups']


class GroupAdminForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['name', 'permissions']
