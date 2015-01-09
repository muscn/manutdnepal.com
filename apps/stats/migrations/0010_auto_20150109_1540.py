# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0009_auto_20150108_2127'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seasondata',
            options={'verbose_name_plural': 'Seasons Data'},
        ),
        migrations.AlterField(
            model_name='seasondata',
            name='matches',
            field=jsonfield.fields.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='seasondata',
            name='summary',
            field=jsonfield.fields.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
