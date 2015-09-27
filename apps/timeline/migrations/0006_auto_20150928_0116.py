# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0005_timelineevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelineevent',
            name='end_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='timelineevent',
            name='start_date',
            field=models.DateField(),
        ),
    ]
