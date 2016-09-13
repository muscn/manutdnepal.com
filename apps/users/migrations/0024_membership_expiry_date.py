# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_renewal_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='expiry_date',
            field=models.DateField(default=datetime.date(2016, 6, 30)),
            preserve_default=False,
        ),
    ]
