# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_esewapayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='esewapayment',
            name='ref_id',
            field=models.CharField(default=1, max_length=25),
            preserve_default=False,
        ),
    ]
