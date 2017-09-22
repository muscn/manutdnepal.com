from django.core.urlresolvers import reverse
from django.db import models
from froala_editor.fields import FroalaField
from versatileimagefield.fields import VersatileImageField

from muscn.utils.forms import unique_slugify
from muscn.utils.location import LocationField
from muscn.utils.mixins import CachedModel


class Partner(CachedModel):
    name = models.CharField(max_length=255)
    partnership = models.CharField(max_length=255, default='Partner')
    slug = models.SlugField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Leave empty/unchanged for default slug.')
    logo = VersatileImageField(upload_to='partners/', blank=True, null=True)
    about = FroalaField(null=True, blank=True)
    privileges = FroalaField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    active = models.BooleanField(default=True)
    location = LocationField(blank=True, max_length=255)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.objects.filter(active=True)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.name)
        super(Partner, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('view_partner', kwargs={'slug': self.slug})

    def get_url(self):
        if self.url:
            return self.url
        else:
            return self.get_absolute_url()
