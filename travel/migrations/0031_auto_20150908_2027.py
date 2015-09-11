# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0030_auto_20150908_0239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='city',
            field=models.CharField(max_length=100, db_index=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='state',
            field=models.CharField(max_length=5, db_index=True),
        ),
    ]
