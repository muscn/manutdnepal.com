# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'O', b'Others')]),
            preserve_default=True,
        ),
    ]
