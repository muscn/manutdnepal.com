# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0020_fixture_broadcast_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stadium',
            name='city',
            field=models.ForeignKey(related_name='stadiums', blank=True, to='stats.City', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='stadium',
            name='slug',
            field=models.SlugField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
