# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('slug', models.SlugField(max_length=254, blank=True)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'photos/', blank=True)),
                ('height', models.FloatField(null=True, blank=True)),
                ('weight', models.FloatField(null=True, blank=True)),
                ('birth_place', models.CharField(max_length=255, null=True, blank=True)),
                ('address', models.CharField(max_length=255, null=True, blank=True)),
                ('phone', models.CharField(max_length=50, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
                ('positions', models.CharField(max_length=50, null=True, blank=True)),
                ('squad_no', models.PositiveIntegerField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('slug', models.SlugField(max_length=254, blank=True)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'photos/', blank=True)),
                ('height', models.FloatField(null=True, blank=True)),
                ('weight', models.FloatField(null=True, blank=True)),
                ('birth_place', models.CharField(max_length=255, null=True, blank=True)),
                ('address', models.CharField(max_length=255, null=True, blank=True)),
                ('phone', models.CharField(max_length=50, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
                ('role', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
