# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(default='M', max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')]),
            preserve_default=False,
        ),
    ]
