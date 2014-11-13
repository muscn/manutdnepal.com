# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='user',
            field=models.OneToOneField(related_name='membership', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
