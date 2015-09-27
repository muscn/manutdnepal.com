# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeline',
            name='slug',
            field=models.SlugField(help_text=b'Leave empty/unchanged for default slug.', max_length=255, null=True, blank=True),
        ),
    ]
