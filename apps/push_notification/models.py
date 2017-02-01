from __future__ import unicode_literals

from django.db import models

class BulkMessage(models.Model):
    message = models.TextField(help_text='Message to broadcast.')
    remarks = models.TextField(null=True, blank=True, help_text='Admin notes.')
    response_message = models.TextField(null=True, blank=True, help_text='Error Message')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    last_sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        # truncate to 75 chars
        char_len = 75
        return (self.message[:char_len] + '..') if len(self.message) > char_len else self.message