# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_cardstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardstatus',
            name='membership',
            field=models.OneToOneField(to='users.Membership'),
            preserve_default=True,
        ),
    ]
