from django.db import models
import datetime
import os

from django.urls import reverse_lazy
from versatileimagefield.fields import VersatileImageField

from apps.events.models import Event
from muscn.utils.forms import unique_slugify


class Album(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Leave empty/unchanged for default slug.')
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ForeignKey('Image', related_name='thumbnail_of', blank=True, null=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now=True)
    event = models.ForeignKey(Event, blank=True, null=True, related_name='albums')

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail
        try:
            return self.images.all()[0]
        except IndexError:
            return None

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(Album, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('album-images', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name or str(self.event)


class Image(models.Model):
    file = VersatileImageField(upload_to='images/')
    album = models.ForeignKey(Album, related_name='images')
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now=True)

    @property
    def file_name(self):
        try:
            return os.path.basename(self.file.file.name)
        except IOError:
            return '-'

    @property
    def file_name_sans_ext(self):
        return os.path.splitext(self.file_name)[0]

    @property
    def title(self):
        return self.name or ''

    # def get_absolute_url(self):
    #     return reverse('view_image', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name or self.file_name
