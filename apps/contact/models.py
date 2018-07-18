# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.postgres.fields import ArrayField
from django.core.mail import mail_admins
from django.db import models

from froala_editor.fields import FroalaField
from solo.models import SingletonModel

from muscn import settings
from muscn.utils.location import LocationField


class ContactSetting(SingletonModel):
    content = FroalaField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    email = ArrayField(models.EmailField(blank=True, null=True), blank=True, null=True)
    phone = ArrayField(models.CharField(max_length=50, blank=True, null=True), blank=True, null=True)
    fax = ArrayField(models.CharField(max_length=50, blank=True, null=True), blank=True, null=True)
    facebook_page = models.URLField(blank=True, null=True)
    facebook_group = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    google_plus = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    location = LocationField(blank=True, null=True)

    @property
    def social_media(self):
        media = []
        if self.facebook_page:
            media.append({'site': 'Facebook', 'url': self.facebook_page, 'fa': 'facebook'})
        if self.facebook_group:
            media.append({'site': 'Facebook Group', 'url': self.facebook_group, 'fa': 'facebook-square'})
        if self.twitter:
            media.append({'site': 'Twitter', 'url': self.twitter, 'fa': 'twitter'})
        if self.instagram:
            media.append({'site': 'Instagram', 'url': self.instagram, 'fa': 'instagram'})
        if self.google_plus:
            media.append({'site': 'Google+', 'url': self.google_plus, 'fa': 'google-plus'})
        if self.linkedin:
            media.append({'site': 'LinkedIn', 'url': self.linkedin, 'fa': 'linkedin'})
        if self.github:
            media.append({'site': 'GitHub', 'url': self.github, 'fa': 'github'})
        return media

    def __str__(self):
        return 'Contact Settings'


class Message(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    message = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def notify(self):
        pass
        # mail_admins(str(self), self.message)

    def __str__(self):
        return 'Message from %s (%s)' % (
            self.name or (self.user.full_name if self.user else 'Unknown'),
            self.email or (self.user.email if self.user else 'Unknown')
        )
