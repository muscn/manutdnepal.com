# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0010_auto_20150928_0306'),
    ]

    operations = [
        migrations.AddField(
            model_name='timelineevent',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to=b'timeline_event_thumbnails/', blank=True),
        ),
    ]
