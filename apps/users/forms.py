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


class MembershipForm(HTML5BootstrapModelForm):
    # date_of_birth = HTML5ModelForm.DateTypeInput()

    gender = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-inline'}), choices=Membership.GENDERS)
    shirt_size = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
                                   choices=Membership.SHIRT_SIZES)
    present_status = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
                                       choices=Membership.PRESENT_STATUSES)
    # identification_type = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
    #                                         choices=Membership.IDENTIFICATION_TYPES)
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=254)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MembershipForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['full_name'].initial = self.user.full_name

    def clean_full_name(self):
        tokens_length = len(self.cleaned_data.get('full_name', '').split())
        if 0 < tokens_length < 2:
            raise forms.ValidationError("Please provide your full name!")
        self.instance.user.full_name = self.cleaned_data['full_name']
        self.instance.user.save()
        return self.cleaned_data['full_name']

    class Meta:
        model = Membership
        exclude = ('status', 'homepage', 'user', 'registration_date', 'approved_date', 'approved_by', 'payment')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            'temporary_address': forms.Textarea(
                attrs={'rows': 2, 'placeholder': 'Temporary Address'}),
            'permanent_address': forms.Textarea(
                attrs={'rows': 2, 'placeholder': 'Permanent Address *'}),

        }


from allauth.account.forms import SignupForm


class SignupForm(SignupForm):
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
    password2 = forms.CharField(widget=forms.PasswordInput, label='Password (again)')

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

    def clean(self):
        data = self.cleaned_data
        if "password1" in data and "password2" in data and data["password1"] != data["password2"]:
            raise forms.ValidationError("Passwords don't match.")

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(username=data['username'], email=data['email'], password=data['password1'])
        user.full_name = data['full_name']
        user.save()
        return user

    class Meta:
        model = User
        exclude = ('last_login', 'is_active', 'is_staff', 'is_superuser', 'groups', 'password')


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