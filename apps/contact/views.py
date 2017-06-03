# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from .forms import ContactForm
from .models import Message, ContactSetting


def contact_us(request):
    if request.method == 'POST':
        data = request.POST.copy()
        if request.user.is_authenticated:
            data['name'] = data['name'] or request.user.full_name or 'Unknown'
            data['email'] = data['email'] or request.user.email or 'Unknown'
        form = ContactForm(data)
        if form.is_valid():
            instance = form.save()
            instance.notify()
            messages.success(request, _('Thank you! Your message has been received.'))
        else:
            messages.error(request, _('Please check the form again.'))
    form = ContactForm()
    obj = ContactSetting.get_solo()
    context = {
        'form': form,
        'obj': obj,
    }
    return render(request, 'contact/contact_us.html', context)
