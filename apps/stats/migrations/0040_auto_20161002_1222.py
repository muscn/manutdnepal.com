# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0039_player_alternative_names'),
    ]

    operations = [
        migrations.AlterField(
            model_name='injury',
            name='type',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
