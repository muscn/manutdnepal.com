from django.core.urlresolvers import reverse
from django.db import models
from froala_editor.fields import FroalaField
from muscn.utils.forms import unique_slugify
from muscn.utils.location import LocationField


class Event(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    organizer = models.CharField(max_length=255, blank=True, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    whole_day_event = models.BooleanField(default=False)
    venue = models.TextField()
    enabled = models.BooleanField(default=True)
    description = FroalaField()
    image = models.ImageField(blank=True, null=True)
    location = LocationField(blank=True, max_length=255)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.title)
        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('view_event', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.title
