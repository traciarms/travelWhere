# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0020_auto_20150903_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='yelp_id',
            field=models.CharField(max_length=50, unique=True, null=True),
        ),
    ]
