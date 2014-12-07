from django import forms
from users.models import User, Membership
from django.contrib.auth.models import Group
from app.libr import HTML5ModelForm


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'is_active',
                  'is_staff', 'is_superuser', 'last_login', 'groups']


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']


class MembershipForm(HTML5ModelForm):
    # SHIRT_SIZES = (
    # ('S', 'Small'),
    # ('M', 'Medium'),
    # ('L', 'Large'),
    # ('XL', 'Extra Large'),
    # ('XXL', 'Double Extra Large'),
    # )
    # date_of_birth = HTML5ModelForm.DateTypeInput()
    SHIRT_SIZES = (
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
        ('XXL', 'XXL'),
    )
    PRESENT_STATUSES = (
        ('S', 'Student'),
        ('E', 'Employed'),
        ('U', 'Unemployed'),
    )
    IDENTIFICATION_TYPES = (
        ('C', 'Citizenship'),
        ('L', 'License'),
        ('I', 'Identity Card'),
    )
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    )
    gender = forms.ChoiceField(widget=forms.RadioSelect(), choices=GENDERS)
    shirt_size = forms.ChoiceField(widget=forms.RadioSelect(), choices=SHIRT_SIZES)
    present_status = forms.ChoiceField(widget=forms.RadioSelect(), choices=PRESENT_STATUSES)
    identification_type = forms.ChoiceField(widget=forms.RadioSelect(), choices=IDENTIFICATION_TYPES)
    full_name = forms.CharField(max_length=254)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MembershipForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].initial = self.user.full_name

    class Meta:
        model = Membership
        exclude = ('membership_status', 'homepage', 'user', 'registration_date')