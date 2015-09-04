# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import travel.models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0026_hotel_hotel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='hotel_id',
            field=travel.models.TruncatingCharField(max_length=150, unique=True, null=True),
        ),
    ]
