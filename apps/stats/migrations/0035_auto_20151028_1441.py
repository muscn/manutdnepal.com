# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0034_auto_20151028_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playersocialaccount',
            name='player',
            field=models.OneToOneField(related_name='social_accounts', to='stats.Player'),
        ),
    ]
