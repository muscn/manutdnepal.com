# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0005_partner_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='partnership',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
