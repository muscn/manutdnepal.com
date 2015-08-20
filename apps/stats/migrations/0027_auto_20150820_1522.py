# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0026_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fixture',
            options={'ordering': ('datetime',)},
        ),
        migrations.AlterField(
            model_name='team',
            name='crest',
            field=models.FileField(null=True, upload_to=b'crests/', blank=True),
        ),
    ]
