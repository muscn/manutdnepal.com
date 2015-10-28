# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0033_playersocialaccount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playersocialaccount',
            name='facebook',
            field=models.CharField(help_text=b'Username', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='playersocialaccount',
            name='instagram',
            field=models.CharField(help_text=b'Username', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='playersocialaccount',
            name='player',
            field=models.ForeignKey(related_name='social_accounts', to='stats.Player'),
        ),
        migrations.AlterField(
            model_name='playersocialaccount',
            name='twitter',
            field=models.CharField(help_text=b'Username', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='playersocialaccount',
            name='website',
            field=models.URLField(help_text=b'URL', max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='playersocialaccount',
            name='youtube',
            field=models.URLField(help_text=b'URL', max_length=255, null=True, blank=True),
        ),
    ]
