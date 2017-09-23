from django import forms
from .models import User, Membership
from django.contrib.auth.models import Group
from muscn.utils.forms import HTML5BootstrapModelForm


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'is_active',
                  'is_staff', 'is_superuser', 'last_login', 'groups']


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']


from allauth.account.forms import SignupForm as AuthSignupForm


class SignupForm(AuthSignupForm):
    full_name = forms.CharField(label='Full name')

    def save(self, request):
        user = super(SignupForm, self).save(request)
        user.full_name = self.cleaned_data['full_name']
        user.save()
        return user

    def signup(self, request, user):
        user.full_name = self.cleaned_data['full_name']
        user.save()


class UserForm(HTML5BootstrapModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')

    # password2 = forms.CharField(widget=forms.PasswordInput, label='Password (again)')

    def clean_username(self):
        data = self.cleaned_data
        try:
            user = User.objects.get(username=data['username'])
            if user == self.instance:
                return data['username']
        except User.DoesNotExist:
            return data['username']
        raise forms.ValidationError('This username is already taken.')

    def clean_email(self):
        data = self.cleaned_data
        try:
            user = User.objects.get(email=data['email'])
            if user == self.instance:
                return data['email']
        except User.DoesNotExist:
            return data['email']
        raise forms.ValidationError('User with this email address already exists.')

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password1'])
        user.full_name = data['full_name']
        user.save()
        return user

    class Meta:
        model = User
        exclude = ('last_login', 'is_active', 'is_staff', 'is_superuser', 'groups', 'password', 'devil_no')


class UserUpdateForm(UserForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

    def save(self):
        data = self.cleaned_data
        user = self.instance
        user.username = data['username']
        user.email = data['email']
        if data['password1'] != '':
            user.set_password(data['password1'])
        user.full_name = data['full_name']
        user.save()
        return user


class MembershipForm(HTML5BootstrapModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=254)

    def clean_full_name(self):
        tokens_length = len(self.cleaned_data.get('full_name', '').split())
        if tokens_length < 2:
            raise forms.ValidationError("Please provide your full name!")
        return self.cleaned_data['full_name']

    class Meta:
        model = User
        fields = ('full_name', 'mobile')
