# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import travel.models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0025_auto_20150904_0443'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='hotel_id',
            field=travel.models.TruncatingCharField(null=True, max_length=150),
        ),
    ]
