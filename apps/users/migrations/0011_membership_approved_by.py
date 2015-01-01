# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_membership_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='approved_by',
            field=models.ForeignKey(related_name='memberships_approved', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
