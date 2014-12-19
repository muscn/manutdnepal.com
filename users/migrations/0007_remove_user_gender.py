# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20141113_0748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='gender',
        ),
    ]
