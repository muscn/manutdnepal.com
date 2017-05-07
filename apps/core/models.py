from django.utils import timezone

from apps.events.models import Event
from apps.post.models import Post
import datetime


def get_featured():
    return Event.objects.filter(start__gt=timezone.now() + datetime.timedelta(days=-1), featured=True).exclude(image__exact='').order_by('start').first() or Post.objects.filter(featured=True).exclude(image__exact='').first()
