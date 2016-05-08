# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0037_fixture_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='time',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
    ]
