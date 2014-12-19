from django.shortcuts import render
from allauth.account.forms import LoginForm, SignupForm

def home(request):
	form = LoginForm()
	signup_form = SignupForm()
	return render(request, 'home.html', {'form': form, 'signup_form': signup_form })
