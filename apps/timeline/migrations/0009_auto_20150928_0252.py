# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0008_auto_20150928_0245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timelineevent',
            name='timelines',
        ),
        migrations.AddField(
            model_name='timeline',
            name='events',
            field=models.ManyToManyField(related_name='timelines', to='timeline.TimelineEvent', blank=True),
        ),
    ]
