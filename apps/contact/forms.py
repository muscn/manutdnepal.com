from django import forms

from muscn.utils.forms import BootstrapModelForm
from .models import Message


class ContactForm(BootstrapModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control full', 'placeholder': 'Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control full', 'placeholder': 'Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control full', 'placeholder': 'Message', 'rows': 2}))

    class Meta:
        model = Message
        fields = ['name', 'email', 'message']
