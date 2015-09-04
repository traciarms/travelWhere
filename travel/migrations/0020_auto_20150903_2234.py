# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import travel.models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0019_auto_20150903_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='eventful_id',
            field=travel.models.TruncatingCharField(max_length=100, null=True, unique=True),
        ),
    ]
