# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms import modelform_factory
from django.shortcuts import render

from .forms import ContactForm
from .models import Message, ContactSetting


def contact_us(request):
    form = ContactForm
    obj = ContactSetting.get_solo()
    context = {
        'form': form,
        'obj': obj
    }
    return render(request, 'contact/contact_us.html', context)
