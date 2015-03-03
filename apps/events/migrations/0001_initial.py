# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True)),
                ('organizer', models.CharField(max_length=255)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(null=True, blank=True)),
                ('whole_day_event', models.BooleanField(default=False)),
                ('venue', models.TextField()),
                ('enabled', models.BooleanField(default=True)),
                ('description', models.TextField()),
                ('image', models.ImageField(null=True, upload_to=b'', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
