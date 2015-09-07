from django.shortcuts import render
from apps.partner.models import Partner


def view_partner(request, slug):
    partner = Partner.objects.get(slug=slug)
    return render(request, 'partner/view_partner.html', {'partner': partner})
