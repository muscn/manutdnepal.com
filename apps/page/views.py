from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .models import Page
from django.shortcuts import render, get_object_or_404


def view_page(request, slug):
    obj = get_object_or_404(Page, slug=slug, status='Published')
    if request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if settings.DEFAULT_FROM_EMAIL:
            receiver = settings.DEFAULT_FROM_EMAIL
        else:
            receiver = 'info@awecode.com'
        if name and email and message:
            try:
                send_mail('Message from' + name, message, email, [receiver], fail_silently=False)
                messages.add_message(request, messages.INFO, 'Your message has been successfully send.')
            except BadHeaderError:
                return HttpResponse('Invalid header Found')
    return render(request, obj.template, {'page': obj})
