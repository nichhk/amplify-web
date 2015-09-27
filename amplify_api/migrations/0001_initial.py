# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(default=b'', unique=True, max_length=100)),
                ('song', models.CharField(default=b'', max_length=100, blank=True)),
                ('master_start', models.DateTimeField(null=True, blank=True)),
                ('slave_start', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('android_id', models.CharField(default=b'', max_length=100, serialize=False, primary_key=True)),
                ('is_master', models.BooleanField(default=False)),
                ('gcm_token', models.CharField(default=b'', max_length=100, null=True, blank=True)),
                ('group', models.ForeignKey(to='amplify_api.Group', null=True)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
