# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0032_auto_20151021_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerSocialAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('twitter', models.CharField(max_length=100, null=True, blank=True)),
                ('instagram', models.CharField(max_length=100, null=True, blank=True)),
                ('facebook', models.CharField(max_length=100, null=True, blank=True)),
                ('youtube', models.URLField(max_length=255, null=True, blank=True)),
                ('website', models.URLField(max_length=255, null=True, blank=True)),
                ('player', models.ForeignKey(to='stats.Player')),
            ],
        ),
    ]
