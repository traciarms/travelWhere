# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0004_auto_20150829_2249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='second_filter',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='third_filter',
        ),
    ]
