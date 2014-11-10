# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20141110_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('temporary_address', models.TextField(null=True)),
                ('permanent_address', models.TextField(null=True)),
                ('homepage', models.URLField(null=True)),
                ('mobile', models.CharField(max_length=50, null=True)),
                ('telephone', models.CharField(max_length=50, null=True, blank=True)),
                ('identification_type', models.CharField(max_length=50, null=True)),
                ('identification_file', models.FileField(null=True, upload_to=b'')),
                ('shirt_size', models.CharField(max_length=4, null=True, choices=[(b'S', b'Small'), (b'M', b'Medium'), (b'L', b'Large'), (b'XL', b'Extra Large'), (b'XXL', b'Double Extra Large')])),
                ('present_status', models.CharField(max_length=1, null=True, choices=[(b'S', b'Student'), (b'E', b'Employed'), (b'U', b'Unemployed')])),
                ('registration_date', models.DateField(null=True)),
                ('approved_date', models.DateField(null=True, blank=True)),
                ('membership_status', models.CharField(max_length=1, null=True, choices=[(b'P', b'Pending'), (b'A', b'Active'), (b'E', b'Expired')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
