# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='date_time',
            field=models.DateTimeField(default=timezone.now),
            preserve_default=True,
        ),
    ]
