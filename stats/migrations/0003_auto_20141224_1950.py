# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_injury_substitution'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='own_goal',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='goal',
            name='penalty',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
