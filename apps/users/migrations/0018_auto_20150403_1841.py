# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20150403_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardstatus',
            name='membership',
            field=models.OneToOneField(related_name='card_status', to='users.Membership'),
            preserve_default=True,
        ),
    ]
