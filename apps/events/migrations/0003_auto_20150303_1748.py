# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20150303_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=froala_editor.fields.FroalaField(),
            preserve_default=True,
        ),
    ]
