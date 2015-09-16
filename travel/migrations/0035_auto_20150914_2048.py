# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0034_auto_20150914_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='img_url',
            field=models.TextField(null=True),
        ),
    ]
