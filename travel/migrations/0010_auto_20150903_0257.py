# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0009_auto_20150902_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='category',
        ),
        migrations.RemoveField(
            model_name='outdoorrecreation',
            name='address',
        ),
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='eventful_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
