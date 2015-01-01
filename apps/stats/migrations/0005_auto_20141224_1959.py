# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0004_injury_injury_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='injury',
            options={'verbose_name_plural': 'Injuries'},
        ),
        migrations.AlterField(
            model_name='injury',
            name='remarks',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='injury',
            name='type',
            field=models.CharField(blank=True, max_length=100, null=True, choices=[(b'Groin', b'Groin'), (b'Hamstring', b'Hamstring'), (b'MCL', b'MCL'), (b'ACL', b'ACL')]),
            preserve_default=True,
        ),
    ]
