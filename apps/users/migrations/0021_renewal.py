# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_auto_20150829_2104'),
        ('users', '0020_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Renewal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('membership', models.ForeignKey(to='users.Membership')),
                ('payment', models.ForeignKey(related_name='renewals', to='payment.Payment')),
            ],
        ),
    ]
