# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0014_auto_20150903_0325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.TextField(null=True),
        ),
    ]
