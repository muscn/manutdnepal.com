# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(help_text=b'Leave empty/unchanged for default slug.', max_length=255, null=True, blank=True)),
                ('content', froala_editor.fields.FroalaField(null=True, blank=True)),
                ('status', models.CharField(default=b'Published', max_length=10, choices=[(b'Published', b'Published'), (b'Draft', b'Draft'), (b'Trashed', b'Trashed')])),
            ],
        ),
    ]
