# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0017_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='color',
            field=models.CharField(default='#000', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='wiki',
            field=models.CharField(default='/', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='official',
            name='image',
            field=models.ImageField(null=True, upload_to=b'photos/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='player',
            name='image',
            field=models.ImageField(null=True, upload_to=b'photos/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='staff',
            name='image',
            field=models.ImageField(null=True, upload_to=b'photos/', blank=True),
            preserve_default=True,
        ),
    ]
