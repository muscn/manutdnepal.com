# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Injury',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, null=True, blank=True)),
                ('return_date', models.DateField(null=True, blank=True)),
                ('return_date_confirmed', models.BooleanField(default=True)),
                ('remarks', models.CharField(max_length=255)),
                ('player', models.ForeignKey(related_name='injuries', to='stats.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Substitution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(blank=True, max_length=10, null=True, choices=[(b'Injury', b'injury'), (b'Tactical', b'tactical')])),
                ('time', models.PositiveIntegerField()),
                ('subbed_in', models.ForeignKey(related_name='subbed_in', to='stats.Player')),
                ('subbed_out', models.ForeignKey(related_name='subbed_out', to='stats.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
