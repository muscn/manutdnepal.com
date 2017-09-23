# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-23 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0033_auto_20170911_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mobile',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('Registered', 'Registered'), ('Pending Payment', 'Pending Payment'), ('Member', 'Member'), ('Expired', 'Expired')], default='Registered', max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='Email address'),
        ),
    ]
