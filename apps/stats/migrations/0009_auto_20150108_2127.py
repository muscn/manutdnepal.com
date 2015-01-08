# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0008_season'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Season',
            new_name='SeasonData',
        ),
    ]
