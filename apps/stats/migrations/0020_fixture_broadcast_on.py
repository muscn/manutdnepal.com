# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0019_auto_20150310_2355'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixture',
            name='broadcast_on',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
