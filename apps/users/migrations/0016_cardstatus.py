# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20150219_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.PositiveIntegerField(default=1, choices=[(1, b'Awaiting Print'), (2, b'Printed'), (3, b'Delivered')])),
                ('remarks', models.CharField(max_length=255, null=True, blank=True)),
                ('membership', models.ForeignKey(to='users.Membership')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
