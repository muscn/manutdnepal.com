# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
        ('users', '0009_auto_20141113_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='payment',
            field=models.ForeignKey(blank=True, to='payment.Payment', null=True),
            preserve_default=True,
        ),
    ]
