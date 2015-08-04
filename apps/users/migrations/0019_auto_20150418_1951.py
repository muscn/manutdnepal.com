# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20150403_1841'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cardstatus',
            options={'verbose_name_plural': 'Card Statuses'},
        ),
        migrations.AlterField(
            model_name='membership',
            name='payment',
            field=models.ForeignKey(related_name='payment_for', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='payment.Payment', null=True),
            preserve_default=True,
        ),
    ]
