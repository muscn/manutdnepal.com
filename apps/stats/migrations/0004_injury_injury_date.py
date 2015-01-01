# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_auto_20141224_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='injury',
            name='injury_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
