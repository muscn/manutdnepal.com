# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-27 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20170525_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=b'events/'),
        ),
    ]
