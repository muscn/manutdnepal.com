from django.db import models


class Timeline(models.Model):
    headline = models.CharField(max_length=255)
    text = models.CharField(max_length=255, blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, null=True)
    credit = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True, upload_to='timeline_thumbnails/')

class Location(models.Model):
    name= models.CharField(max_length=255)
    icon = models.ImageField(blank=True, null=True, upload_to='timeline_locations/')
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    zoom = models.PositiveSmallIntegerField(default=10)


class TimelineEvent(Timeline):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)