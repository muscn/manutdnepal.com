# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0010_auto_20150109_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionYearMatches',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('matches', jsonfield.fields.JSONField()),
                ('competition_year', models.ForeignKey(to='stats.CompetitionYear')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
