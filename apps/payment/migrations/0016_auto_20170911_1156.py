# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-11 06:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0015_auto_20170719_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankdeposit',
            name='voucher_image',
            field=models.ImageField(upload_to='voucher_images/'),
        ),
        migrations.AlterField(
            model_name='directpayment',
            name='receipt_image',
            field=models.ImageField(blank=True, null=True, upload_to='receipt_images/'),
        ),
        migrations.AlterField(
            model_name='directpayment',
            name='receipt_no',
            field=models.PositiveIntegerField(null=True, unique=True, verbose_name='Receipt No. (If you paid directly to a representative)'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='date_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date/Time'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='By'),
        ),
    ]
