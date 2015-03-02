# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0014_auto_20150302_2053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='official',
            name='previous_club',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='previous_club',
        ),
        migrations.AddField(
            model_name='player',
            name='on_loan',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='squad_no',
            field=models.PositiveIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
