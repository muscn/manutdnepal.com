# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0007_auto_20150928_0146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timelineevent',
            name='timeline',
        ),
        migrations.AddField(
            model_name='timelineevent',
            name='timelines',
            field=models.ManyToManyField(related_name='events', to='timeline.Timeline'),
        ),
    ]
