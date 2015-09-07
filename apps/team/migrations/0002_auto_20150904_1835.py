# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='address',
        ),
        migrations.RemoveField(
            model_name='player',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='player',
            name='name',
        ),
        migrations.RemoveField(
            model_name='player',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='address',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='date_of_birth',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='name',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='phone',
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staff',
            name='user',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
