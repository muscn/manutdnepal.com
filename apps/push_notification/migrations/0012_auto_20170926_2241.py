# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-26 16:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('push_notification', '0011_auto_20170926_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdevice',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='devices', to=settings.AUTH_USER_MODEL),
        ),
    ]