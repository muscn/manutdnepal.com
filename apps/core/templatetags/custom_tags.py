from django import template
from django.urls import reverse

from apps.stats.models import Competition

register = template.Library()


@register.simple_tag
def active_nav(request, url):
    if request.path == reverse(url):
        return 'active'
    return ''

@register.assignment_tag
def get_active_leagues():
    return Competition.get_ls_active()