# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0011_auto_20150903_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(null=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.CharField(null=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='event',
            name='venue_name',
            field=models.CharField(null=True, max_length=100),
        ),
    ]
