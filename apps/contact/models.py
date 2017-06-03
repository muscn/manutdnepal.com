# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.postgres.fields import ArrayField
from django.db import models

from froala_editor.fields import FroalaField
from solo.models import SingletonModel

from muscn.utils.location import LocationField


class Contact(SingletonModel):
    content = FroalaField(null=True, blank=True)
    email = ArrayField(models.EmailField(blank=True, null=True))
    phone = ArrayField(models.CharField(max_length=50, blank=True, null=True))
    fax = ArrayField(models.CharField(max_length=50, blank=True, null=True))
    facebook_page = models.URLField(blank=True, null=True)
    facebook_group = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    google_plus = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    location = LocationField(blank=True, null=True)


class Message(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'Message from %s' % self.name
