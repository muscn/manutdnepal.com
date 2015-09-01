# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0029_auto_20150901_0138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='competition',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='competition',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='competition',
            name='short_name',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
