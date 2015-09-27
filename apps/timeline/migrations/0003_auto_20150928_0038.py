# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0002_timeline_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timeline',
            old_name='caption',
            new_name='media_caption',
        ),
        migrations.RenameField(
            model_name='timeline',
            old_name='credit',
            new_name='media_credit',
        ),
        migrations.RenameField(
            model_name='timeline',
            old_name='url',
            new_name='media_url',
        ),
        migrations.AddField(
            model_name='timelineevent',
            name='location',
            field=models.ForeignKey(related_name='events', blank=True, to='timeline.Location', null=True),
        ),
        migrations.AddField(
            model_name='timelineevent',
            name='timeline',
            field=models.ForeignKey(related_name='events', default=1, to='timeline.Timeline'),
            preserve_default=False,
        ),
    ]
