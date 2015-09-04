# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import travel.models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0021_restaurant_yelp_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='nightlife',
            name='yelp_id',
            field=models.CharField(max_length=50, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='yelp_id',
            field=travel.models.TruncatingCharField(max_length=50, unique=True, null=True),
        ),
    ]
