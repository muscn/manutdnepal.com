# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0013_auto_20150109_2236'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seasondata',
            options={'ordering': ('-year',), 'verbose_name_plural': 'Seasons Data'},
        ),
        migrations.AddField(
            model_name='official',
            name='birth_place',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='official',
            name='height',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='official',
            name='previous_club',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='official',
            name='weight',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='birth_place',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='height',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='previous_club',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='weight',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='staff',
            name='birth_place',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='staff',
            name='height',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='staff',
            name='previous_club',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='staff',
            name='weight',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='official',
            name='slug',
            field=models.SlugField(max_length=254, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='slug',
            field=models.SlugField(max_length=254, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='staff',
            name='slug',
            field=models.SlugField(max_length=254, blank=True),
            preserve_default=True,
        ),
    ]
