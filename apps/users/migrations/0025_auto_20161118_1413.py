# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_membership_expiry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='renewal',
            name='approved_by',
            field=models.ForeignKey(related_name='renewals_approved', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='renewal',
            name='approved_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
