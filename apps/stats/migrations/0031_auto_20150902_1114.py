# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0030_auto_20150901_1647'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competitionyear',
            options={'ordering': ('competition__order',)},
        ),
        migrations.AlterField(
            model_name='injury',
            name='type',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
