# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0013_auto_20150109_2236'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seasondata',
            options={'ordering': ('-year',), 'verbose_name_plural': 'Seasons Data'},
        ),
    ]
