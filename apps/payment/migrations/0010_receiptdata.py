# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_auto_20150829_2104'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceiptData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('from_no', models.IntegerField()),
                ('to_no', models.IntegerField()),
            ],
        ),
    ]
