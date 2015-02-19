# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_auto_20150216_0320'),
    ]

    operations = [
        migrations.CreateModel(
            name='EsewaPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
                ('pid', models.CharField(max_length=255)),
                ('tax_amount', models.FloatField(default=0)),
                ('service_charge', models.FloatField(default=0)),
                ('delivery_charge', models.FloatField(default=0)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('details', jsonfield.fields.JSONField()),
                ('payment', models.OneToOneField(related_name='esewa_payment', to='payment.Payment')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
