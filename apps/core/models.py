from django.utils import timezone
from django.core.cache import cache

from apps.events.models import Event
from apps.post.models import Post
import datetime


def get_featured():
    featured = cache.get('featured')
    if not featured:
        featured = Event.objects.filter(start__gt=timezone.now() + datetime.timedelta(days=-1), featured=True).exclude(
            image__exact='').order_by('start').first() or Post.objects.filter(featured=True).exclude(image__exact='').first()
        cache.set('featured', featured)
    return featured
