from __future__ import unicode_literals
import uuid
from django.db import models
from django.core.cache import cache


class DistributedKey(models.Model):
    key = models.TextField(blank=True, help_text='Leave blank for auto-generation.')
    client_name = models.CharField(max_length=250)

    @staticmethod
    def set_keys():
        data = [obj.key for obj in DistributedKey.objects.all()]
        cache.set('distributed_keys', data)
        return data

    @staticmethod
    def keys():
        cached = cache.get('distributed_keys')
        if not cached:
            cached = DistributedKey.set_keys()
        return cached

    def __str__(self):
        return str(self.key) + '| ' + self.client_name

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = uuid.uuid4().hex
        super(DistributedKey, self).save(*args, **kwargs)
        DistributedKey.set_keys()
