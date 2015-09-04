# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0015_auto_20150903_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='address',
            field=models.TextField(null=True),
        ),
    ]
