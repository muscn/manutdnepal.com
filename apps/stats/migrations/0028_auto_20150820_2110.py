# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0027_auto_20150820_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixture',
            name='mufc_score',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='fixture',
            name='opponent_score',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='fixture',
            name='remarks',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
