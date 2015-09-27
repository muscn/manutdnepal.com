from django.db import models
from muscn.utils.forms import unique_slugify


class Timeline(models.Model):
    headline = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Leave empty/unchanged for default slug.')
    text = models.CharField(max_length=255, blank=True, null=True)
    media_caption = models.CharField(max_length=255, blank=True, null=True)
    media_credit = models.CharField(max_length=255, blank=True, null=True)
    media_url = models.URLField(blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True, upload_to='timeline_thumbnails/')
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.headline

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.headline)
        super(Timeline, self).save(*args, **kwargs)


class Location(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(blank=True, null=True, upload_to='timeline_locations/')
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    zoom = models.PositiveSmallIntegerField(default=10)


class TimelineEvent(models.Model):
    headline = models.CharField(max_length=255)
    text = models.CharField(max_length=255, blank=True, null=True)
    media_caption = models.CharField(max_length=255, blank=True, null=True)
    media_credit = models.CharField(max_length=255, blank=True, null=True)
    media_url = models.URLField(blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    location = models.ForeignKey(Location, related_name='events', blank=True, null=True)
    timeline = models.ForeignKey(Timeline, related_name='events')

    def __str__(self):
        return self.headline
