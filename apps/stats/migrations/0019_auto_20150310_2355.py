# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0018_auto_20150306_0147'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fixture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_home_game', models.BooleanField(default=True)),
                ('datetime', models.DateTimeField()),
                ('round', models.CharField(max_length=255, null=True, blank=True)),
                ('venue', models.CharField(help_text=b'Leave blank for auto-detection', max_length=255, null=True, blank=True)),
                ('competition_year', models.ForeignKey(to='stats.CompetitionYear')),
                ('opponent', models.ForeignKey(to='stats.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='team',
            name='color',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='team',
            name='wiki',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
