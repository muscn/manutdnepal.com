from django.db import models
from muscn.utils.flexible_date import FlexibleDateField
from muscn.utils.forms import unique_slugify


class Location(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(blank=True, null=True, upload_to='timeline_locations/')
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    zoom = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return self.name


class TimelineEvent(models.Model):
    headline = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    media_caption = models.CharField(max_length=255, blank=True, null=True)
    media_credit = models.CharField(max_length=255, blank=True, null=True)
    media_url = models.URLField(blank=True, null=True)
    start_date = FlexibleDateField()
    end_date = FlexibleDateField(blank=True, null=True)
    location = models.ForeignKey(Location, related_name='events', blank=True, null=True)

    def __str__(self):
        return self.headline


class Timeline(models.Model):
    headline = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Leave empty/unchanged for default slug.')
    text = models.TextField(blank=True, null=True)
    media_caption = models.CharField(max_length=255, blank=True, null=True)
    media_credit = models.CharField(max_length=255, blank=True, null=True)
    media_url = models.URLField(blank=True, null=True)
    thumbnail = models.ImageField(blank=True, null=True, upload_to='timeline_thumbnails/')
    enabled = models.BooleanField(default=True)
    events = models.ManyToManyField(TimelineEvent, related_name='timelines', blank=True)

    def serialize(self):
        dct = {'title': {'media': {}, 'text': {'headline': self.headline}}, 'events': []}
        if self.media_url:
            dct['title']['media']['url'] = self.media_url
        if self.media_caption:
            dct['title']['media']['caption'] = self.media_caption
        if self.media_credit:
            dct['title']['media']['credit'] = self.media_credit
        if self.text:
            dct['title']['text']['text'] = self.text
        for event in self.events.all():
            event_dct = {'media': {}, 'text': {'headline': event.headline}}
            if event.media_url:
                event_dct['media']['url'] = event.media_url
            if event.media_caption:
                event_dct['media']['caption'] = event.media_caption
            if event.media_credit:
                event_dct['media']['credit'] = event.media_credit
            if event.text:
                event_dct['text']['text'] = event.text
            event_dct['start_date'] = {'year': event.start_date.split('-')[0]}
            try:
                event_dct['start_date']['month'] = event.start_date.split('-')[1]
                try:
                    event_dct['start_date']['day'] = event.start_date.split('-')[2]
                except IndexError:
                    pass
            except IndexError:
                pass
            if event.end_date:
                event_dct['end_date'] = {'year': event.end_date.split('-')[0]}
                try:
                    event_dct['end_date']['month'] = event.end_date.split('-')[1]
                    try:
                        event_dct['end_date']['day'] = event.end_date.split('-')[2]
                    except IndexError:
                        pass
                except IndexError:
                    pass
            dct['events'].append(event_dct)

        return dct

    def __str__(self):
        return self.headline

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.headline)
        super(Timeline, self).save(*args, **kwargs)
