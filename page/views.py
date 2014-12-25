from page.models import Page
from django.shortcuts import render, get_object_or_404


def view_page(request, slug):
    obj = get_object_or_404(Page, slug=slug, status='Published')
    return render(request, obj.template, {'page': obj})
