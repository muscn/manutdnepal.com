# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0028_auto_20150820_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='match',
            field=models.ForeignKey(related_name='goals', to='stats.Fixture'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='time',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
