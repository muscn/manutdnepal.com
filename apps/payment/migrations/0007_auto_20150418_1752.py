# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='directpayment',
            name='receipt_image',
            field=models.ImageField(null=True, upload_to=b'receipt_images/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='directpayment',
            name='received_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
