# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-11 06:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_remove_page_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(blank=True, help_text='Leave empty/unchanged for default slug.', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='status',
            field=models.CharField(choices=[('Published', 'Published'), ('Draft', 'Draft'), ('Trashed', 'Trashed')], default='Published', max_length=10),
        ),
    ]
