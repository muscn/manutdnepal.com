# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('icon', models.ImageField(null=True, upload_to=b'timeline_locations/', blank=True)),
                ('lat', models.FloatField(null=True, blank=True)),
                ('long', models.FloatField(null=True, blank=True)),
                ('zoom', models.PositiveSmallIntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='Timeline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('headline', models.CharField(max_length=255)),
                ('text', models.CharField(max_length=255, null=True, blank=True)),
                ('caption', models.CharField(max_length=255, null=True, blank=True)),
                ('credit', models.CharField(max_length=255, null=True, blank=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('thumbnail', models.ImageField(null=True, upload_to=b'timeline_thumbnails/', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TimelineEvent',
            fields=[
                ('timeline_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='timeline.Timeline')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True, blank=True)),
            ],
            bases=('timeline.timeline',),
        ),
    ]
