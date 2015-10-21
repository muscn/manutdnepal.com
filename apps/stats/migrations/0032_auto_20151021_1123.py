# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0031_auto_20150902_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='injury',
            name='return_date_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
