# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20141113_0758'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='gender',
            field=models.CharField(max_length=1, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='present_status',
            field=models.CharField(max_length=1, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='shirt_size',
            field=models.CharField(max_length=4, null=True),
            preserve_default=True,
        ),
    ]
