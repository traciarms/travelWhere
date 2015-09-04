# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0010_auto_20150903_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='url',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='nightlife',
            name='url',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='url',
            field=models.CharField(max_length=250),
        ),
    ]
