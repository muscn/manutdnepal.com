# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20150106_2202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='identification_type',
        ),
        migrations.AlterField(
            model_name='membership',
            name='identification_file',
            field=models.FileField(null=True, upload_to=b'identification_files/'),
            preserve_default=True,
        ),
    ]
