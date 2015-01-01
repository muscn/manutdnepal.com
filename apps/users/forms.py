from django import forms
from .models import User, Membership
from django.contrib.auth.models import Group
from app.utils.forms import HTML5BootstrapModelForm


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
    gender = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-inline'}), choices=GENDERS)
    shirt_size = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-inline'}), choices=SHIRT_SIZES)
    present_status = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
                                       choices=PRESENT_STATUSES)
    identification_type = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-inline'}),
                                            choices=IDENTIFICATION_TYPES)
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=254)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MembershipForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].initial = self.user.full_name

    def clean_full_name(self):
        tokens_length = len(self.cleaned_data.get('full_name', '').split())
        if 0 < tokens_length < 2:
            raise forms.ValidationError("Please provide your full name!")

    class Meta:
        model = Membership
        exclude = ('status', 'homepage', 'user', 'registration_date')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),
            'temporary_address': forms.Textarea(
                attrs={'rows': 2, 'placeholder': 'Temporary Address'}),
            'permanent_address': forms.Textarea(
                attrs={'rows': 2, 'placeholder': 'Permanent Address'}),

        }