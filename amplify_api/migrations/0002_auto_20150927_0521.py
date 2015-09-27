# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amplify_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gcm_token',
            field=models.CharField(default=b'', max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(default=b'', unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='oauth',
            field=models.CharField(default=b'', max_length=200, serialize=False, primary_key=True, blank=True),
        ),
    ]
