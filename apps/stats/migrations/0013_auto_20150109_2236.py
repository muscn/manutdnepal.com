# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0012_remove_seasondata_matches'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competitionyearmatches',
            old_name='matches',
            new_name='matches_data',
        ),
    ]
