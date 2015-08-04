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

    @property
    def status(self):
        self.start = self.start.replace(tzinfo=None)
        if self.end:
            self.end = self.end.replace(tzinfo=None)
        from datetime import datetime

        now = datetime.now()

        if self.end and now > self.end:
            return 'past'
        if not self.end and now.date() > self.start.date():
            return 'past'
        if now < self.start:
            return 'future'
        # return 'present'
        if self.whole_day_event and self.start.date() == now.date():
            return 'present'
        if now > self.start and not self.end and self.start.date() == now.date():
            return 'present'
        if self.end and self.start < now < self.end:
            return 'present'

    def save(self, *args, **kwargs):
        unique_slugify(self, self.title)
        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('view_event', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.title
