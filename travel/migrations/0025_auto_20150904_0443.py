# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import travel.models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0024_remove_nightlife_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nightlife',
            name='yelp_id',
            field=travel.models.TruncatingCharField(null=True, unique=True, max_length=50),
        ),
    ]
