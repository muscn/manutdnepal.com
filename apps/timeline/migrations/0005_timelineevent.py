# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0004_auto_20150928_0053'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimelineEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('headline', models.CharField(max_length=255)),
                ('text', models.CharField(max_length=255, null=True, blank=True)),
                ('media_caption', models.CharField(max_length=255, null=True, blank=True)),
                ('media_credit', models.CharField(max_length=255, null=True, blank=True)),
                ('media_url', models.URLField(null=True, blank=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('location', models.ForeignKey(related_name='events', blank=True, to='timeline.Location', null=True)),
                ('timeline', models.ForeignKey(related_name='events', to='timeline.Timeline')),
            ],
        ),
    ]
