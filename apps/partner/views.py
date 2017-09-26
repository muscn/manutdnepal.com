from django.shortcuts import render, get_object_or_404
from apps.partner.models import Partner


def view_partner(request, slug):
    partner = get_object_or_404(Partner, slug=slug)
    return render(request, 'partner/view_partner.html', {'partner': partner})
