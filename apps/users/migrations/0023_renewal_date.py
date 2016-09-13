# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20160913_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='renewal',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
