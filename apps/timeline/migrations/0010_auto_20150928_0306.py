# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0009_auto_20150928_0252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeline',
            name='text',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='timelineevent',
            name='text',
            field=models.TextField(null=True, blank=True),
        ),
    ]
