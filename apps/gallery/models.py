from django.db import models
import datetime
import os
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
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)
    event = models.ForeignKey(Event, blank=True, null=True, related_name='albums')

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail
        try:
            return self.images.all()[0]
        except IndexError:
            return None

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.datetime.today()
        self.updated_at = datetime.datetime.today()
        unique_slugify(self, self.name)
        super(Album, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse_lazy('view_album', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name or str(self.event)


class Image(models.Model):
    file = models.ImageField(upload_to='images/')
    album = models.ForeignKey(Album, related_name='images')
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

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

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.datetime.today()
        self.updated_at = datetime.datetime.today()
        super(Image, self).save(*args, **kwargs)

    def __str__(self):
        return self.name or self.file_name

# Create your models here.
