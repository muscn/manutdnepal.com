from django import forms
from django.db import models
from django.conf import settings


class LocationPickerWidget(forms.TextInput):
    class Media:
        css = {
            'all': (
                'events/location_picker.css',
            )
        }
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.js',
            'https://maps.googleapis.com/maps/api/js?v=3&sensor=true',
            'events/jquery.location_picker.js',
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(LocationPickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        if None == attrs:
            attrs = {}
        attrs['class'] = 'location_picker'
        return super(LocationPickerWidget, self).render(name, value, attrs)


class LocationField(models.CharField):
    def formfield(self, **kwargs):
        kwargs['widget'] = LocationPickerWidget
        return super(LocationField, self).formfield(**kwargs)