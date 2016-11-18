# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0010_receiptdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptdata',
            name='remarks',
            field=models.TextField(null=True, blank=True),
        ),
    ]
