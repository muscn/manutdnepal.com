from django.shortcuts import render
from allauth.account.forms import LoginForm, SignupForm


def home(request):
    login_form = LoginForm()
    signup_form = SignupForm()
    return render(request, 'home.html', {'login_form': login_form, 'signup_form': signup_form})
