# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_renewal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renewal',
            name='membership',
            field=models.ForeignKey(related_name='renewals', to='users.Membership'),
        ),
    ]
