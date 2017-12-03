import datetime

from django.urls import reverse
from django.db import models
from django.core.cache import cache

from froala_editor.fields import FroalaField
from versatileimagefield.fields import VersatileImageField

from apps.events.models import Event
from apps.gallery.models import Album
from apps.stats.models import Fixture
from muscn.utils.forms import unique_slugify
from muscn.utils.mixins import CachedModel


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Leave empty/unchanged for default slug.')
    content = FroalaField(null=True, blank=True)
    statuses = (
        ('Published', 'Published'), ('Draft', 'Draft'), ('Trashed', 'Trashed'))
    status = models.CharField(
        max_length=10,
        choices=statuses,
        default='Published')
    created_at = models.DateTimeField(blank=True)
    image = VersatileImageField(blank=True, null=True, upload_to='post_images')
    featured = models.BooleanField(default=True)
    match = models.ForeignKey(Fixture, blank=True, null=True, related_name='posts')
    event = models.ForeignKey(Event, blank=True, null=True, related_name='posts')
    album = models.ForeignKey(Album, blank=True, null=True, related_name='posts')
    url = models.URLField(blank=True, null=True)

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status='Published')

    @property
    def date(self):
        return self.created_at

    @classmethod
    def recent(cls, count=10):
        return cls.objects.filter(status='Published')[0:count]

    def excerpt(self):
        txt = self.content
        if len(txt) < 101:
            return txt
        return txt[0:98] + ' ...'

    def save(self, *args, **kwargs):
        cache.delete('featured')
        unique_slugify(self, self.title)
        if not self.id:
            self.created_at = datetime.datetime.today()
        super().save(*args, **kwargs)
        if self.featured:
            from apps.events.models import Event
            Post.objects.exclude(pk=self.pk).update(featured=False)
            Event.objects.all().update(featured=False)

    def get_absolute_url(self):
        return self.url or reverse('view_post', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)
