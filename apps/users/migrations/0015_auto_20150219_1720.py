# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20150216_0320'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='present_status',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='shirt_size',
        ),
    ]
