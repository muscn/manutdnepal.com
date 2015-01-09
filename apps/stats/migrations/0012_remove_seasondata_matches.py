# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0011_competitionyearmatches'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seasondata',
            name='matches',
        ),
    ]
