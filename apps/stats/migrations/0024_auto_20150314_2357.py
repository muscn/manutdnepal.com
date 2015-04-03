# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0023_auto_20150311_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='stadium',
            field=models.ForeignKey(related_name='teams', blank=True, to='stats.Stadium', null=True),
            preserve_default=True,
        ),
    ]
