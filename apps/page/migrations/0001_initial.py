# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import froala_editor.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=255, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name=b'children', blank=True, to='page.Category', null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(help_text=b'Leave empty/unchanged for default slug.', max_length=255, null=True, blank=True)),
                ('content', froala_editor.fields.FroalaField(null=True, blank=True)),
                ('template', models.CharField(max_length=255, null=True, blank=True)),
                ('status', models.CharField(default=b'Published', max_length=10, choices=[(b'Published', b'Published'), (b'Draft', b'Draft'), (b'Trashed', b'Trashed')])),
                ('comments_enabled', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(to='page.Category', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
