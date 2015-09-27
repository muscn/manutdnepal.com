# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0003_auto_20150928_0038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timelineevent',
            name='location',
        ),
        migrations.RemoveField(
            model_name='timelineevent',
            name='timeline',
        ),
        migrations.RemoveField(
            model_name='timelineevent',
            name='timeline_ptr',
        ),
        migrations.AddField(
            model_name='timeline',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='TimelineEvent',
        ),
    ]
