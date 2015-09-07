# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(help_text=b'Leave empty/unchanged for default slug.', max_length=255, null=True, blank=True)),
                ('logo', models.FileField(null=True, upload_to=b'partners/', blank=True)),
                ('about', froala_editor.fields.FroalaField(null=True, blank=True)),
                ('privileges', froala_editor.fields.FroalaField(null=True, blank=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
    ]
