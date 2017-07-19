from __future__ import unicode_literals
import uuid
from django.db import models


class DistributedKey(models.Model):
    key = models.TextField(blank=True)
    client_name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.key) + '| ' + self.client_name

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = uuid.uuid4().hex
        return super(DistributedKey, self).save(*args, **kwargs)
