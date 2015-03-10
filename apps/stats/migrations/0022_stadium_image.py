# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0021_auto_20150311_0102'),
    ]

    operations = [
        migrations.AddField(
            model_name='stadium',
            name='image',
            field=models.ImageField(null=True, upload_to=b'/stadiums/', blank=True),
            preserve_default=True,
        ),
    ]
