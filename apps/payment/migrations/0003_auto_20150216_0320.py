# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20150104_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankdeposit',
            name='payment',
            field=models.OneToOneField(related_name='bank_deposit', to='payment.Payment'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='directpayment',
            name='payment',
            field=models.OneToOneField(related_name='direct_payment', to='payment.Payment'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='payment',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Date/Time'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(verbose_name=b'By', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
