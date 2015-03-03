from django.db import models
from muscn.utils.forms import unique_slugify


class Event(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)
    organizer = models.CharField(max_length=255, blank=True, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    whole_day_event = models.BooleanField(default=False)
    venue = models.TextField()
    enabled = models.BooleanField(default=True)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)

    def save(self, *args, **kwargs):
        unique_slugify(self, self.title)
        super(Event, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title
