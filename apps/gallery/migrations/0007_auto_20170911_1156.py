# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-11 06:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0006_auto_20170527_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
