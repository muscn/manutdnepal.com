# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20141207_1908'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='membership',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='user',
            name='devil_no',
            field=models.PositiveIntegerField(unique=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='gender',
            field=models.CharField(max_length=1, null=True, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'O', b'Others')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='homepage',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='identification_type',
            field=models.CharField(max_length=50, null=True, choices=[(b'C', b'Citizenship'), (b'L', b'License'), (b'I', b'Identity Card')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='payment',
            field=models.ForeignKey(related_name='payment_for', blank=True, to='payment.Payment', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='present_status',
            field=models.CharField(max_length=1, null=True, choices=[(b'S', b'Student'), (b'E', b'Employed'), (b'U', b'Unemployed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='registration_date',
            field=models.DateField(default=datetime.datetime.now, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='shirt_size',
            field=models.CharField(max_length=4, null=True, choices=[(b'S', b'S'), (b'M', b'M'), (b'L', b'L'), (b'XL', b'XL'), (b'XXL', b'XXL')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='temporary_address',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
