# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import muscn.utils.flexible_date


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0006_auto_20150928_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelineevent',
            name='end_date',
            field=muscn.utils.flexible_date.FlexibleDateField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='timelineevent',
            name='start_date',
            field=muscn.utils.flexible_date.FlexibleDateField(max_length=250),
        ),
    ]
