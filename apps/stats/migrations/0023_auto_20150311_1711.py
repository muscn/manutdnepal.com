# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0022_stadium_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mufc_score', models.PositiveIntegerField(default=0)),
                ('opponent_score', models.PositiveIntegerField(default=0)),
                ('fixture', models.ForeignKey(to='stats.Fixture')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='stadium',
            name='image',
            field=models.ImageField(null=True, upload_to=b'stadiums/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='team',
            name='crest',
            field=models.ImageField(null=True, upload_to=b'crests/', blank=True),
            preserve_default=True,
        ),
    ]
