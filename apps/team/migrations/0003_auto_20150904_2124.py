# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_auto_20150904_1835'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ('order',)},
        ),
        migrations.AlterModelOptions(
            name='staff',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='player',
            name='remarks',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='staff',
            name='remarks',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
