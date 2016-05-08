# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0036_auto_20160115_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixture',
            name='data',
            field=jsonfield.fields.JSONField(null=True, blank=True),
        ),
    ]
