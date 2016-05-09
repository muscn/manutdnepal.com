# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0038_auto_20160508_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='alternative_names',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
