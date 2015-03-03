# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import muscn.utils.location


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150303_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location',
            field=muscn.utils.location.LocationField(max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
